from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# 初始化Flask应用，并配置数据库连接
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost/student"
# app.config['SQLALCHEMY_ECHO'] = True  # 一般在生产环境中建议设置为False

# 初始化SQLAlchemy
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'  # 指定数据库表名为'user'
    id = db.Column(db.Integer, primary_key=True)  # 主键id
    student_number = db.Column(db.String(30), nullable=False)  # 学号列，不可为空
    account = db.Column(db.String(30), nullable=False)  # 账号列，不可为空
    password = db.Column(db.String(80), unique=True)  # 密码列，唯一约束

    def __init__(self, student_number, account, password):
        """
        用户模型初始化方法
        :param student_number:  用户学号
        :param account: 用户账号
        :param password: 用户密码（未加密）
        """
        self.student_number = student_number
        self.account = account
        # self.password = generate_password_hash(password)  # 使用哈希函数加密密码
        self.password = password  # 使用哈希函数加密密码

    def check_password(self, password):
        """
        检查密码是否正确
        :param password: 输入的密码
        :return: 布尔值，表示密码是否正确
        """
        # return check_password_hash(self.password, password)  # 检查密码是否正确
        return self.password, password

    @staticmethod
    def is_valid_input(student_number, account, password, password2):
        """
        校验输入是否有效
        :param student_number: 学号
        :param account: 账号
        :param password: 密码
        :param password2: 确认密码
        :return: 布尔值，输入是否有效
        """
        if not all([student_number, account, password, password2]):
            return False
        if password != password2:
            return False
        return True


# 主页路由
@app.route('/')
def index():
    return render_template('index.html')


# 注册路由
@app.route("/register", methods=['get', 'post'])
def register():
    """
    用户注册接口
    :return: 注册页面或重定向到注册页面或登录页面
    """
    if request.method == 'POST':
        # 获取并校验表单数据
        student_number = request.form.get('student_number')
        account = request.form.get('account')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        # 输入校验
        if not User.is_valid_input(student_number, account, password, password2):
            return redirect(url_for('register'))

        # 账号存在性校验
        if User.query.filter_by(account=account).first():
            return redirect(url_for('register'))

        # 新用户添加到数据库
        try:
            new_user = User(student_number, account, password)
            db.session.add(new_user)
            db.session.commit()
            print("用户添加成功")
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Error: {e}")
            db.session.rollback()
            return redirect(url_for('register'))

    return render_template('register.html')


# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    用户登录接口
    :return: 登录页面或重定向到登录页面或登录成功信息
    """
    if request.method == 'POST':
        # 获取并校验表单数据
        student_number = request.form.get('student_number')
        account = request.form.get('account')
        password = request.form.get('password')

        # 数据不完整校验
        if not account or not password or not student_number:
            return redirect(url_for('login'))

        # 账号密码匹配校验
        user = User.query.filter_by(account=account).first()
        if user and user.check_password(password):
            print("登录成功")
            return render_template('/index.html')
        else:
            return redirect(url_for('login'))

    return render_template('login.html')


# 创建数据表
with app.app_context():
    db.create_all()  # 创建表，仅在首次运行或删除数据库文件后需要

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5563, debug=True)