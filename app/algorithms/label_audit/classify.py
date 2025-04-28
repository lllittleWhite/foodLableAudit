import json
from openai import OpenAI
import os

def bot_classify_food(food_label):
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
    audit_reference = open("app/algorithms/audit_reference/分类表.txt", "r", encoding="utf-8").read()

    system_prompt = f"""
    你是一个食品分类专家，请你根据食品分类表对食品标签信息进行分类，并输出分类结果json。
    注意：分到最细级别
    
    食品分类表：
    {audit_reference}
    
    EXAMPLE JSON OUTPUT:
    {{
        "分类码": "",  // 一串数字
        "备注": ""  // 分类理由
    }}
    """

    user_prompt = "待审核内容：" + food_label

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
    raw_food_label = "".join(string_list)
    print(bot_classify_food(raw_food_label))

