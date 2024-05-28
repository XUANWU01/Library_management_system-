# 导入SQLAlchemy相关模块，用于定义数据模型和操作数据库
from sqlalchemy import Column, Integer, String, create_engine, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker

from flask_sqlalchemy import SQLAlchemy
# 创建链接
db = SQLAlchemy()

# 定义File类，它继承自Base，表示数据库中的'files'表
class File(db.Model):
    """
    表示存储在数据库中的文件信息。
    
    属性:
    - id: 文件的唯一标识符，主键
    - filename: 文件名，不允许为空
    - file_path: 文件在服务器上的完整路径，不允许为空
    - uploaded_at: 文件上传的时间，使用服务器当前时间作为默认值
    """
    __tablename__ = 'files'  # 指定映射到的数据库表名

    id = Column(Integer, primary_key=True)  # 自增整数ID
    filename = Column(String(255), nullable=False)  # 不可为空的文件名，最大长度255个字符
    file_path = Column(String(1024), nullable=False)  # 不可为空的文件路径，最大长度1024个字符
    uploaded_at = Column(TIMESTAMP, server_default=func.now())  # 文件上传时间，默认为服务器当前时间


