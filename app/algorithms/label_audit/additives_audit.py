import sys
import os
import asyncio
import json
from openai import OpenAI
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))

from app.utils.pdf_content_get import load_pdf_content_as_string, load_pdf_pages


def bot_get_additive_index(raw_food_label):
    """
    查找食品标签中添加剂的索引

    参数：
    string: 待审核食品标签信息

    返回值：
    json: 添加剂索引json
    """
    # 使用deepseek api
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    # 审核依据表：
    # audit_reference = open("app/algorithms/audit_reference/GB7718-2011整理.txt", "r", encoding="utf-8").read()

    content_string = asyncio.run(load_pdf_content_as_string(1, 10, "app/algorithms/audit_reference/添加剂索引表.pdf"))
    system_prompt = f"""
    你是一个添加剂索引查找专家，请你根据添加剂索引表，查找我提供给你的食品标签文本中添加剂的页码和紧挨着的添加剂页码，即我想要知道这个添加剂在它第一页和最后一页的页码，并输出为JSON格式。
    
    注意：食品标签中的添加剂可能是中文名称也可能是INS号，如果是INS号，在索引表中找中文名，输出json时要输出中文名
    
    添加剂索引表：
    {content_string}
    
    EXAMPLE JSON OUTPUT:
    {{
        "添加剂索引": [
            {{
                "添加剂名称": "茶黄素",
                "start_page": "25", 
                "end_page": "26"
            }},
            {{
                "添加剂名称": "二氧化硫及亚硫酸盐",
                "start_page": "33",
                "end_page": "35"
            }},
            ...
        ]
    }}
    """

    user_prompt = f"""找出食品标签中添加剂在pdf中给出的页码范围,食品标签信息: {raw_food_label}"""

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={
            'type': 'json_object'
        }
    )

    audit_result = json.loads(response.choices[0].message.content)

    return audit_result

def get_reference_content(page_index_json):
    '''
    获取添加剂适用食物参考依据

    参数：
    page_index_json: 添加剂索引json

    返回值：
    string: 添加剂适用食物参考依据
    '''
    reference_content = "";
    additive_name = "";

    for additive in page_index_json['添加剂索引']:
        start_page = int(additive['start_page']) + 3
        end_page = int(additive['end_page']) + 3

        content_string = asyncio.run(load_pdf_content_as_string(start_page, end_page))
        reference_content += content_string
        additive_name += additive['添加剂名称']

    return reference_content, additive_name

def get_table_a2_content():
    '''
    获取表A.2内容

    返回值：
    string: 表A.2内容
    '''
    a2_content_string = asyncio.run(load_pdf_content_as_string(1, 2, "app/algorithms/audit_reference/添加剂表A2.pdf"))
    return a2_content_string

def bot_additives_audit(raw_food_label, reference_content, additive_name):
    """
    对食品标签信息进行审核

    参数：
    string: 待审核食品标签信息

    返回值：
    json: 审核结果json
    """
    # 使用deepseek api
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    # 审核依据表：
    audit_reference = reference_content
    a2_content = get_table_a2_content()

    system_prompt = f"""
    你是一个食品标签添加剂审核专家，请你根据添加剂适用食物参考依据，对食品标签中使用的添加剂进行审核，并输出为JSON格式。
    该食品使用到的添加剂为：{additive_name}

    添加剂适用食物参考依据：
    {audit_reference}
    
    可能用到的表A.2 （表A.1中例外食品编号对应的食品类别）：
    {a2_content}

    EXAMPLE JSON OUTPUT:
    {{
        "审核结果": [
            {{
                "审核项": "", // 添加剂名称
                "是否通过": "通过/不通过",
                "原因": "" // 备注
            }},
            {{
                "审核项": "", // 添加剂名称
                "是否可添加": "通过/不通过",
                "原因": ""
            }},
            ...
        ]
    }}
    """

    user_prompt = "待审核内容：" + raw_food_label

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        response_format={
            'type': 'json_object'
        }
    )

    audit_result = json.loads(response.choices[0].message.content)

    for item in audit_result["审核结果"]:
        item["具体内容"] = ""

    return audit_result

def audit_additive_main(food_label):
    page_index_json = bot_get_additive_index(food_label)
    reference_content, additive_name = get_reference_content(page_index_json)
    audit_result = bot_additives_audit(food_label, reference_content, additive_name)
    return audit_result


if __name__ == "__main__":
    string_list = [
        "**千层派(饼干)",
        "配料:面粉、棕榈油、氢化棕榈仁油、葡萄干、椰子粉、白砂糖、蔓越莓、食用盐、麦芽糖粉、食用香料、抗氧化剂(维生素E)、着色剂(β-胡萝卜素)",
        "生产企业:**食品股份有限公司",
        "地址:江苏省连云港市******",
        "联系方式:0518-******",
        "产品标准代号:GB/T20980-2021",
        "食品生产许可证编号:SC11822******",
        "生产日期:日/月/年(见包装喷码)",
        "保质期:日/月/年(见包装喷码)",
        "贮存条件:请置于阴凉干燥处，开封后尽快食用。",
        "净含量:80g",
        "营养成分表"
    ]
    food_label = "".join(string_list)
    audit_result = audit_additive_main(food_label)
    print(audit_result)



