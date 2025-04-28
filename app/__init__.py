from flask import Flask
import os
from app.config.config import config

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 确保上传目录存在
    for folder in [app.config['UPLOAD_FOLDER'], app.config['LAWS_FOLDER']]:
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    # 注册蓝图
    from app.api.label import label_bp
    from app.api.ocr import ocr_bp
    from app.api.translation import translation_bp
    from app.api.comparison import comparison_bp
    from app.api.laws import laws_bp
    
    app.register_blueprint(label_bp)
    app.register_blueprint(ocr_bp)
    app.register_blueprint(translation_bp)
    app.register_blueprint(comparison_bp)
    app.register_blueprint(laws_bp)
    
    return app 