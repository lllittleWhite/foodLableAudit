import json


if __name__ == "__main__":
# 原始JSON数据
    data = {
        '审核结果': [
            {
                '添加剂': '维生素E',
                '是否可添加': '是',
                '备注': '根据GB2760-2024，维生素E作为抗氧化剂可用于焙烤食品，最大使用量按生产需要适量使用。'
            },
            {
                '添加剂': 'β-胡萝卜素',
                '是否可添加': '是',
                '备注': '根据GB2760-2024，β-胡萝卜素作为着色剂可用于焙烤食品，最大使用量为1.0g/kg。'
            }
        ]
    }

    # 转换为二维数组
    # result = [[str(item)] for item in data['审核结果']]
    # result = [[json.dumps(item, ensure_ascii=False)] for item in data['审核结果']]
    # result = [[str(item) for item in sublist.items()] for sublist in data['审核结果']]
    # result = [[str(item) for item in sublist.values()] for sublist in data['审核结果']]
    # result = [[str(item) for item in sublist.items()] for sublist in data['审核结果']]
    result = [[f"{k}: {v}" for k, v in sublist.items()] for sublist in data['审核结果']]



    print(result)