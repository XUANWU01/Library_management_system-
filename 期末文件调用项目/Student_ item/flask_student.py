from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from demo_mysql import User, db
import os

# 初始化Flask应用
app = Flask(__name__)
# 1.添加密钥
# app.secret_key = '123456'

# 使用 db 对象 连接数据库
# 连接参数：  mysql+python://用户名:密码@连接地址/数据库名
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost/student"
# 用于 显示 SQLalchemy 的执行过程
app.config['SQLALCHEMY_ECHO'] = False

db.init_app(app)

# 设置上传文件的存储目录
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 检查上传文件夹是否存在，若不存在则创建
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


# 主页路由
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload_file')
def upload_file():
    return render_template('upload.html')


# 文件上传路由，只处理POST请求
@app.route('/upload', methods=['POST'])
def uploaded_file():
    # 检查请求中是否有文件部分
    if 'file' not in request.files:
        return 'No file part in the request', 400

    # 获取上传的文件
    file = request.files['file']

    # 如果没有选择文件，浏览器会提交一个空文件部分
    if file.filename == '':
        return '未选择文件', 400

    # 判断文件是否允许上传
    if file and allowed_file(file.filename):
        # 使用werkzeug库的secure_filename函数确保文件名安全
        filename = file.filename

        # 保存上传的文件到指定的目录
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # 返回成功消息
        return redirect(url_for('index'))

    # 文件类型不允许
    else:
        return '无效的文件类型', 400


# 定义允许文件上传的辅助函数，这里为了简化示例，允许所有文件类型
def allowed_file(filename):
    # 在实际应用中，应限制允许上传的文件类型
    return True


# 添加下载文件的路由
@app.route('/downloads/<filename>')
def download_file(filename):
    # 使用send_from_directory发送文件，设置as_attachment=True以便下载
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


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
            print("输入不合法")
            return redirect(url_for('register'))

        # 账号存在性校验
        if db.session.query(User.account).filter(User.account == account).first():
            print("账号已存在")
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
        print('student_number:', student_number, 'account:', account, 'password:', password)
        # 数据不完整校验
        if not account or not password or not student_number:
            return redirect(url_for('login'))

        # 账号密码匹配校验
        user = db.session.query(User.student_number, User.password).filter(User.student_number == student_number).first()
        print(user)
        if user[1] == password:

            # flash('登录成功', 'success')
            # # 仅限于登录成功时，保存session信息
            # session['login_status'] = True
            print("登录成功")
            return render_template('/index.html')
        else:
            # flash('用户名或密码错误', 'danger')
            print("登录失败")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/show')
def show():
    # 显示所有账号
    result = db.session.query(User.account).all()
    return render_template('show.html', result123=result)


# 添加基本的错误处理和日志记录。
# import logging
# logging.basicConfig(filename='app.log', level=logging.INFO)
#一般没有上线项目可以不要日志



@app.errorhandler(404)
def page_not_found(e):
    logging.error(f"404错误：{e}")
    return render_template('404.html'), 404

# 创建数据表
with app.app_context():
    db.create_all()  # 创建表，仅在首次运行或删除数据库文件后需要

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5563, debug=True)
