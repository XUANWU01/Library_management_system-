from flask import Flask, request, render_template, send_from_directory
import os

# 初始化Flask应用
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 设置上传文件的存储目录
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 检查上传文件夹是否存在，若不存在则创建
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 主页路由，返回上传文件的HTML模板
@app.route('/')
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
        return 'No selected file', 400

    # 判断文件是否允许上传
    if file and allowed_file(file.filename):
        # 使用werkzeug库的secure_filename函数确保文件名安全
        filename = secure_filename(file.filename)

        # 保存上传的文件到指定的目录
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # 返回成功消息
        return 'File {} uploaded successfully!'.format(filename)

    # 文件类型不允许
    else:
        return 'Invalid file type', 400

# 定义允许文件上传的辅助函数，这里为了简化示例，允许所有文件类型
def allowed_file(filename):
    # 在实际应用中，应限制允许上传的文件类型
    return True

# 添加下载文件的路由
@app.route('/downloads/<filename>')
def download_file(filename):
    # 使用send_from_directory发送文件，设置as_attachment=True以便下载
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# 应用启动
if __name__ == '__main__':
    # 启动调试模式
    app.run(debug=True)
