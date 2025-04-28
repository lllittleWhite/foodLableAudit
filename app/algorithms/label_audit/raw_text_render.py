import json
from openai import OpenAI
import os
# 提取审核要素
def bot_render_text(string_list):
    """
    整理原始食品标签文本

    参数：
    list(str): 待提取文本str列表

    返回值：
    str: 整理后的标签文本
    """
    elements = ""
    
    # 将string_list转化为string
    raw_food_label = "".join(string_list)
    # bot: 得到结构化数据 / 简单整理 / 不需要太严格
    # 使用deepseek api

    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )

    system_prompt = """
    你是一个食品标签信息整理引擎，请根据ocr识别的食品标签，重新整理文本，使语序通顺没有错别字，不要增加不存在的内容，直接返回整理后的标签信息即可，不要说多余的话。
    """

    user_prompt = raw_food_label

    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        # response_format={
        #     'type': 'json_object'
        # }
    )

    # elements = json.loads(response.choices[0].message.content)
    elements = response.choices[0].message.content

    return elements

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
    print(bot_render_text(string_list))
