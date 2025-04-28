import uuid
import os
from werkzeug.utils import secure_filename
from flask import current_app

def generate_uuid():
    """生成UUID"""
    return str(uuid.uuid4())

def save_file(file, folder=None):
    """保存上传的文件并返回文件路径"""
    if file.filename == '':
        return None
        
    filename = secure_filename(file.filename)
    storage_folder = folder or current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(storage_folder, filename)
    file.save(file_path)
    return file_path 