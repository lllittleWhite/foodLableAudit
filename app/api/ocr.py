from flask import Blueprint, request, jsonify
from app.utils.helpers import generate_uuid, save_file

ocr_bp = Blueprint('ocr', __name__)

# 2. OCR图像识别接口
@ocr_bp.route('/TextAndSheet', methods=['POST'])
def ocr_text_and_sheet():
    if 'file' not in request.files:
        return jsonify({"code": 400, "msg": "没有上传文件", "data": None})
    
    file = request.files['file']
    method = request.form.get('method', 'blur')
    
    if file.filename == '':
        return jsonify({"code": 400, "msg": "未选择文件", "data": None})
    
    # 保存上传的文件
    file_path = save_file(file)
    
    # 由于OCR识别未实现，返回一个样例响应
    response = {
        "code": 200,
        "msg": "成功",
        "data": {
            "Sheet": [["项目", "含量", "NRV%"], ["能量", "420kJ", "5%"], ["蛋白质", "10g", "20%"]],
            "Content": ["产品名称：XX食品", "配料：面粉、水、糖", "净含量：100g", "保质期：12个月"]
        },
        "entryId": generate_uuid()
    }
    
    return jsonify(response) 