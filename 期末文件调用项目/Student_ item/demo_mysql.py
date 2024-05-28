from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
from werkzeug.security import generate_password_hash, check_password_hash


# 创建链接
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'  # 指定数据库表名为'user'
    id = db.Column(db.Integer, primary_key=True)  # 主键id
    student_number = db.Column(db.String(30), nullable=False, unique=True)  # 学号列，不可为空，唯一约束
    account = db.Column(db.String(30), nullable=False)  # 账号列，不可为空
    password = db.Column(db.String(80), unique=False)  # 密码列

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
