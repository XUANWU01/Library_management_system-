from flask_sqlalchemy import SQLAlchemy
# from flask_login import app
from sqlalchemy import Column, String, Integer


# 创建链接
db = SQLAlchemy()


class Test(db.Model):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True)
    account = Column(String(30), nullable=False)
    password = Column(String(8), unique=True)

    def __init__(self, account, password):
        self.account = account
        self.password = password
