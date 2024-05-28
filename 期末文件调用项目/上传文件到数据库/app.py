from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, session
import os
from Demo_sql import File, db
import secrets

app = Flask(__name__)

# 从配置文件中读取密钥和其他配置
app.config['SECRET_KEY'] = secrets.token_hex(32)  # 强随机密钥
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost/student"
app.config['SQLALCHEMY_ECHO'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db.init_app(app)

# 确保上传文件夹存在
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 创建数据表
with app.app_context():
    db.create_all()
@app.route('/upload_file')
def upload_file():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def uploaded_file():
    """
    该函数处理文件上传，从请求中获取文件，保存到文件系统，并将信息存储到数据库中。
    """
    if 'file' not in request.files:
        return 'No file part in the request', 400

    file = request.files['file']

    # 实际项目中应进一步完善文件类型检查
    if not file or not allowed_file(file.filename):
        return 'Invalid file type', 400

    # 生成唯一的文件名以避免覆盖现有文件
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # 使用流式写入提高性能
    # with open(file_path, 'wb') as f:
    #     for chunk in file.chunks():
    #         f.write(chunk)

    try:
        file_record = File(filename=filename, file_path=file_path)
        db.session.add(file_record)
        db.session.commit()
        print(f"File '{file_record.filename}' uploaded successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.session.rollback()
    finally:
        db.session.close()

    return '上传成功', 200


def allowed_file(filename):
    # 示例：只允许图片上传，实际应用中应根据需求调整
    return True

def secure_filename(filename):
    # 注意：这只是一个基础的实现，实际应用中可能需要更复杂的逻辑来确保文件名的安全性
    return filename.replace(' ', '_')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5563, debug=True)
