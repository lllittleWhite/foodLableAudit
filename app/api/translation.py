from flask import Blueprint, request, jsonify
from app.utils.helpers import generate_uuid, save_file

translation_bp = Blueprint('translation', __name__)

# 3. 图像翻译接口
@translation_bp.route('/Translation', methods=['POST'])
def translation():
    if 'file' not in request.files:
        return jsonify({"code": 400, "msg": "没有上传文件", "data": None})
    
    file = request.files['file']
    method = request.form.get('method', 'blur')
    
    if file.filename == '':
        return jsonify({"code": 400, "msg": "未选择文件", "data": None})
    
    # 保存上传的文件
    file_path = save_file(file)
    
    # 由于翻译未实现，返回一个样例响应
    response = {
        "code": 200,
        "msg": "成功",
        "data": {
            "Sheet": [["Item", "Content", "NRV%"], ["Energy", "420kJ", "5%"], ["Protein", "10g", "20%"]],
            "Content": ["Product Name: XX Food", "Ingredients: Flour, Water, Sugar", "Net Weight: 100g", "Shelf Life: 12 months"]
        },
        "entryId": generate_uuid()
    }
    
    return jsonify(response) 