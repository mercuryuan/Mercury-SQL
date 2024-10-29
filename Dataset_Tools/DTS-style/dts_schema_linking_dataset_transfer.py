import pandas as pd
import json
import re
from config import BASE_DIR
import pandas as pd

# 读取CSV文件

csv_path = f"{BASE_DIR}/Data/DTS-data/training/filtered_finetuning_dataset.csv"  # 请替换为实际的CSV文件路径
data = pd.read_csv(csv_path)

# 存储生成的JSON数据
output_data = []

# 遍历CSV中的每一行数据
for index, row in data.iterrows():
    # 定义 instruction
    instruction = "Filter out the most streamlined database schema based on a given problem."

    # 去除换行符、冗余空格，并替换转义字符
    question = row['question'].replace('""', '"')

    # 添加一个database_ID,我认为至关重要
    db_id = row['db_id']

    # 用正则表达式替换多余空格，使 schema 压缩为一行并保持整洁
    full_schema = re.sub(r'\s+', ' ', row['database_schema']).replace('\"', '"')
    filtered_schema = re.sub(r'\s+', ' ', row['filtered_database_schema']).replace('\"', '"')

    # 定义input和output字段
    input_text = f"###Question: {question},###Database_ID:{db_id},###Full_database_schema: {full_schema}"
    output_text = filtered_schema

    # 创建一个字典结构用于存储该条数据
    entry = {
        "instruction": instruction,
        "input": input_text,
        "output": output_text
    }

    # 将该条数据添加到输出数据列表中
    output_data.append(entry)

# 将结果保存为JSON文件
json_path = f"{BASE_DIR}/Training_Dataset/DTS/dts_schema_linking_DDLform.json"  # 输出文件路径
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print(f"DDL风格的schema linking微调JSON数据集已保存至 {json_path}")
