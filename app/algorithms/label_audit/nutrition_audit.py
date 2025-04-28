import json
from openai import OpenAI
import os

def bot_nutrition_audit(food_label, nutrition_table):
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
    audit_reference = open("app/algorithms/audit_reference/GB28050-2011整理.txt", "r", encoding="utf-8").read()

    system_prompt = f"""
    你是一个食品营养标签信息审核专家，请你根据审核依据表的审核项目依次对食品营养标签信息进行审核，并输出为JSON格式。
    
    注意：
    1、审核项一共有5项，分别为：
       - 成分强制标示
       - 成分表格式审核
       - NRV计算
       - 功能声称
       - 含量声称
       
    如果标签中没有功能声称和含量声称，则无需审核，直接通过。
    
    你审核时，需要根据审核依据表对这5个审核项目依次进行审核，审核顺序要正确，不要遗漏，输出时，需要按照这5个审核项的顺序输出。
    
    2、忽略错别字，只关注内容即可
    
    审核依据表：
    {audit_reference}
    
    EXAMPLE JSON OUTPUT:
    {{
        "审核结果": [
            {{
                "审核项": "成分强制标示",
                "是否通过": "通过/不通过", 
                "原因": "原因"  // 不通过写原因，通过则写通过
            }},
            {{
                "审核项": "成分表格式审核",
                "是否通过": "通过/不通过",
                "原因": "原因"
            }},
            ...
        ]
    }}
    """

    user_prompt = "待审核内容：食品标签信息：" + food_label + "\n" + "营养成分表：" + nutrition_table

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

def array_to_markdown(array):
    header = "| " + " | ".join(array[0]) + " |"
    separator = "| " + " | ".join(["---"] * len(array[0])) + " |"
    rows = []
    for row in array[1:]:
        rows.append("| " + " | ".join(str(x) for x in row) + " |")
    return "\n".join([header, separator] + rows)


if __name__ == "__main__":
    string_list = """
    | 项目         | 每100克 | NRV%   |
    |--------------|---------|--------|
    | 能量         | 2300千焦 | 27%    |
    | 蛋白质       | 6.5克   | 11%    |
    | 脂肪         | 34.0克  | 57%    |
    | 饱和脂肪     | 20.5克  | 103%   |
    | 反式脂肪     | 0.2克   | -      |
    | 碳水化合物   | 55.0克  | 18%    |
    | 钠           | 345毫克 | 18%    |
    """
    raw_food_label = "".join(string_list)
    print(bot_nutrition_audit(raw_food_label))