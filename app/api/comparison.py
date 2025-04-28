from flask import Blueprint, request, jsonify, current_app
from app.utils.helpers import generate_uuid, save_file
import base64
import os

comparison_bp = Blueprint('comparison', __name__)

# 4. 图像对比接口
@comparison_bp.route('/TextComparison', methods=['POST'])
def text_comparison():
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({"code": 400, "msg": "缺少文件", "data": None})
    
    file1 = request.files['file1']
    file2 = request.files['file2']
    method = request.form.get('method', 'Comparison')
    
    # 保存上传的文件
    file_path1 = save_file(file1)
    file_path2 = save_file(file2)
    
    if not file_path1 or not file_path2:
        return jsonify({"code": 400, "msg": "文件保存失败", "data": None})
    
    # 图像对比未实现，返回一个样例响应
    # 简单的base64编码图片
    with open(file_path1, 'rb') as f:
        img1_base64 = base64.b64encode(f.read()).decode('utf-8')
    with open(file_path2, 'rb') as f:
        img2_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    response = {
        "code": 200,
        "msg": "成功",
        "data": {
            "Text1": ["产品名称：XX食品", "配料：面粉、水、糖", "净含量：100g"],
            "Text2": ["产品名称：XX食品", "配料：面粉、水、糖、盐", "净含量：120g"],
            "Result": ["相同", "不同: 增加了'盐'成分", "不同: 100g -> 120g"],
            "ModifiedImage1": img1_base64[:100] + "...",  # 截取部分base64，避免响应过大
            "ModifiedImage2": img2_base64[:100] + "..."
        },
        "entryId": generate_uuid()
    }
    
    return jsonify(response) 