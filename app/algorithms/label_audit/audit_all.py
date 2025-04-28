from app.algorithms.label_audit.raw_text_render import bot_render_text
from app.algorithms.label_audit.classify import bot_classify_food
from app.algorithms.label_audit.text_audit import bot_text_audit
from app.algorithms.label_audit.nutrition_audit import bot_nutrition_audit, array_to_markdown
from app.algorithms.label_audit.additives_audit import audit_additive_main


def audit_GeneralCheck(string_list, string_list_list, check_type, type1, type2, type3, self_type):
    # 1. 整理标签
    food_label = bot_render_text(string_list)

    print(food_label)

    # 2. 食品分类
    food_type = str(bot_classify_food(food_label))

    print(food_type)

    # 3. 标签文本格式审核
    general_audit_result = bot_text_audit(food_label)

    print(general_audit_result)

    # 4. 添加剂审核
    additives_audit_result = audit_additive_main(food_label)

    print(additives_audit_result)

    # 5. 组装审核json格式
    audit_result = {
        "audit_result": [
            {
                "审核标准": "G7718-2011",
                "审核结果": general_audit_result["审核结果"]
            },
            {
                "审核标准": "GB2760-2024",
                "审核结果": additives_audit_result["审核结果"]
            }
        ]
    }
    return audit_result, food_type

def audit_SheetCheck(string_list, string_list_list, check_type, type1, type2, type3, self_type):
    # 1. 整理标签
    food_label = bot_render_text(string_list)

    print(food_label)

    nutrition_table = array_to_markdown(string_list_list)

    print(nutrition_table)

    # 2. 食品分类
    food_type = str(bot_classify_food(food_label))

    print(food_type)

    # 3. 营养标签审核
    nutrition_audit_result = bot_nutrition_audit(food_label, nutrition_table)

    print(nutrition_audit_result)

    # 4. 组装审核json格式
    audit_result = {
        "audit_result": [
            {
                "审核标准": "G28050-2011",
                "审核结果": nutrition_audit_result["审核结果"]
            }
        ]
    }
    return audit_result, food_type


# def audit_all(string_list, string_list_list, check_type, type1, type2, type3, self_type):
#     # 1. 整理标签
#     food_label = bot_render_text(string_list)
#     nutrition_table = array_to_markdown(string_list_list)

#     print(food_label)
#     # 2. 食品分类
#     food_type = str(bot_classify_food(food_label))

#     print(food_type)

#     # 3. 标签文本格式审核
#     general_audit_result = bot_text_audit(food_label)

#     print(general_audit_result)

#     audit_result = ["G7718-2011食品标签通则审核："]
#     audit_result.extend(
#         f"{k}: {v}" 
#         for sublist in general_audit_result['审核结果'] 
#         for k, v in sublist.items()
#     )

#     # 4. 营养标签审核
#     nutrition_audit_result = bot_nutrition_audit(food_label, nutrition_table)

#     print(nutrition_audit_result)

#     audit_result.append("营养标签审核：")
#     audit_result.extend(
#         f"{k}: {v}" 
#         for sublist in nutrition_audit_result['审核结果'] 
#         for k, v in sublist.items()
#     )

#     # 5. 添加剂审核
#     additives_audit_result = audit_additive_main(food_label)

#     print(additives_audit_result)

#     audit_result.append("添加剂审核：")
#     audit_result.extend(
#         f"{k}: {v}" 
#         for sublist in additives_audit_result['审核结果'] 
#         for k, v in sublist.items()
#     )

#     return audit_result, food_type