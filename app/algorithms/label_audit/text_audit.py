import json
from openai import OpenAI
import os

def bot_text_audit(raw_food_label):
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
    audit_reference = open("app/algorithms/audit_reference/GB7718-2011整理.txt", "r", encoding="utf-8").read()

    system_prompt = f"""
    你是一个食品标签信息审核专家，请你根据审核依据表的审核项目依次对食品标签信息进行审核，并输出为JSON格式。
    
    注意：
    1、审核项一共有10项，为生产日期、保质期、贮存条件、食品名称、配料表、净含量与规格、食品生产许可证编号、产品标准代号、生产者/经销商信息、添加剂格式。
    你审核时，需要根据审核依据表对这十个审核项目依次进行审核，审核顺序要正确，不要遗漏，输出时，需要按照这10个审核项的顺序输出。
    
    2、忽略错别字，只关注内容即可
    
    审核依据表：
    {audit_reference}
    
    EXAMPLE JSON OUTPUT:
    {{
        "审核结果": [
            {{
                "审核项": "生产日期",
                "是否通过": "通过/不通过", 
                "原因": "原因",  // 不通过写原因，通过则写通过
                "具体内容": "具体内容"  // 写标签中对应的原内容
            }},
            {{
                "审核项": "保质期",
                "是否通过": "通过/不通过",
                "原因": "原因",
                "具体内容": "具体内容"
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
    a = """
{
    {
        "审核标准": "GB7718-2011",
        "审核结果": [
            {
                "审核项": "生产日期",
                "是否通过": "通过",
                "原因": "通过",
                "具体内容": "日/月/年(见包装喷码)"
            }
        ]
    },
    {
        "审核标准": "GB2818-2011",
        "审核结果": [
            {
                "审核项": "生产日期",
                "是否通过": "通过",
                "原因": "通过",
                "具体内容": "日/月/年(见包装喷码)"
            }
        ]
    },
    {
        "审核标准": "GB2760-2024",
        "审核结果": [
            {
                "审核项": "生产日期",
                "是否通过": "通过",
                "原因": "通过",
                "具体内容": "日/月/年(见包装喷码)"
            }
        ]
    }
}
"""
    raw_food_label = "".join(string_list)
    print(bot_text_audit(raw_food_label))