from flask import Blueprint, request, jsonify
from app.utils.helpers import generate_uuid
from app.algorithms.label_audit.audit_all import audit_GeneralCheck, audit_SheetCheck
label_bp = Blueprint('label', __name__)

# 1. 标签审核接口
@label_bp.route('/LabelCheck/TextAndSheet', methods=['POST'])
def label_check():
    data = request.json
    
    # 从请求中获取参数
    string_list = data.get('StringList', [])
    string_list_list = data.get('StringListList', [])
    check_type = data.get('CheckType', 'GeneralCheck')
    type1 = data.get('Type1', '')
    type2 = data.get('Type2', '')
    type3 = data.get('Type3', '')
    self_type = data.get('Self', '')
    

    # 调用算法接口
    # audit_result_list,fodd_type = audit_all(string_list, string_list_list, check_type, type1, type2, type3, self_type)

    # 判断check_type 
    if check_type == 'GeneralCheck':
        audit_result_list,fodd_type = audit_GeneralCheck(string_list, string_list_list, check_type, type1, type2, type3, self_type)
    elif check_type == 'SheetCheck':
        audit_result_list,fodd_type = audit_SheetCheck(string_list, string_list_list, check_type, type1, type2, type3, self_type)

    response = {
        "code": 200,
        "msg": "成功",
        "data": {
            "audit_result": audit_result_list["audit_result"],  # 简单返回原文本
            "type1": type1,
            "type2": type2,
            "type3": type3,
            "self": fodd_type
        },
        "entryId": generate_uuid()
    }

    # 测试
    # response = {
    #     "code": 200,
    #     "msg": "成功",
    #     "data": {
    #         "stringList": string_list,  # 简单返回原文本
    #         "type1": type1,
    #         "type2": type2,
    #         "type3": type3,
    #         "self": self_type
    #     },
    #     "entryId": generate_uuid()
    # }
    
    return jsonify(response) 