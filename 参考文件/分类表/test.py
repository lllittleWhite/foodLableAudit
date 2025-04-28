import json

def process_json_file(input_file, output_file):
    """从JSON文件中读取数据，移除标准号字段，保存到新文件"""
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    processed_data = []
    for item in data:
        new_item = {k: v for k, v in item.items() if k != "是否有标签要求"} #是否有标签要求、标准号
        processed_data.append(new_item)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, indent=2, ensure_ascii=False)
    
    print(f"处理完成，结果已保存到 {output_file}")

import json

def remove_no_label_required_entries(input_file, output_file):
    """
    从JSON文件中删除所有"是否有标签要求": "无"的条目
    
    :param input_file: 输入JSON文件路径
    :param output_file: 输出JSON文件路径
    """
    # 读取原始JSON文件
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 过滤掉"是否有标签要求": "无"的条目
    filtered_data = [
        entry for entry in data 
        if not (entry.get("是否有标签要求") == "无")
    ]
    
    # 写入新的JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(filtered_data, f, ensure_ascii=False, indent=2)
    
    original_count = len(data)
    filtered_count = len(filtered_data)
    removed_count = original_count - filtered_count
    
    print(f"处理完成：原始数据 {original_count} 条，过滤后 {filtered_count} 条，移除 {removed_count} 条")
    print(f"结果已保存到: {output_file}")


# 示例使用
if __name__ == "__main__":
    # 假设这是您的原始JSON数据
    # 删除标准号
    process_json_file('参考文件/分类表/低优先级最简.json', '参考文件/分类表/test.json')
    
    # 删除 无标签要求项
    # remove_no_label_required_entries('参考文件/分类表/低优先级简.json', '参考文件/分类表/低优先级最简.json')