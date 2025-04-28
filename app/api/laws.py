from flask import Blueprint, request, jsonify, send_file, current_app
from app.utils.helpers import save_file
import os
from datetime import datetime

laws_bp = Blueprint('laws', __name__)

# 5. 法规检索接口
@laws_bp.route('/LawsSearch', methods=['POST'])
def laws_search():
    data = request.json
    keyword = data.get('word', '')
    
    # 法规搜索未实现，返回样例
    search_results = [
        {
            "FileName": "食品安全法.pdf",
            "PageNumber": 5,
            "BeforeText": "根据相关规定，食品生产企业应当",
            "Keyword": keyword,
            "AfterText": "相关标准，确保食品安全。"
        },
        {
            "FileName": "食品标签管理规定.pdf",
            "PageNumber": 12,
            "BeforeText": "食品标签应当清晰标示",
            "Keyword": keyword,
            "AfterText": "等相关信息，不得含有虚假内容。"
        }
    ]
    
    return jsonify(search_results)

# 6. 法规文件上传接口
@laws_bp.route('/zsk-api/open/prepack/addFoodRegula', methods=['POST'])
def add_food_regula():
    # 检查请求头中的appId
    app_id = request.headers.get('appId')
    if app_id != 'ZSK':
        return jsonify({
            "Code": 401,
            "Msg": "未授权，缺少有效的appId",
            "Data": None,
            "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "ExecuteTime": "100ms"
        })
    
    title = request.form.get('title', '')
    num = request.form.get('num', '')
    product_name = request.form.get('productName', '')
    
    # 处理上传的文件
    if 'files' not in request.files:
        return jsonify({
            "Code": 400,
            "Msg": "没有上传文件",
            "Data": None,
            "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "ExecuteTime": "50ms"
        })
    
    files = request.files.getlist('files')
    file_names = []
    
    for file in files:
        if file.filename == '':
            continue
        
        file_path = save_file(file, current_app.config['LAWS_FOLDER'])
        if file_path:
            file_names.append(os.path.basename(file_path))
    
    response = {
        "Code": 200,
        "Msg": "成功",
        "Data": f"已上传{len(file_names)}个文件：{', '.join(file_names)}",
        "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "ExecuteTime": "200ms"
    }
    
    return jsonify(response)

# 7. 法规文件下载接口
@laws_bp.route('/hn/fileDownload', methods=['GET'])
def file_download():
    file_id = request.args.get('fileid', '')
    app_id = request.args.get('appid', '')
    
    if app_id != 'ZSK':
        return jsonify({"error": "未授权，缺少有效的appId"}), 401
    
    # 这里假设文件ID对应法规文件夹中的文件名
    # 实际应用中可能需要从数据库查找文件ID对应的实际文件路径
    
    # 由于没有实际文件，生成一个示例PDF文件
    sample_pdf_path = os.path.join(current_app.config['LAWS_FOLDER'], f"{file_id}.pdf")
    
    # 检查文件是否存在，如果不存在则创建一个简单的示例文件
    if not os.path.exists(sample_pdf_path):
        # 这里应该实际创建一个PDF文件，但为了简化，我们只返回一个错误
        return jsonify({"error": f"文件ID {file_id} 不存在"}), 404
    
    return send_file(sample_pdf_path, as_attachment=True) 