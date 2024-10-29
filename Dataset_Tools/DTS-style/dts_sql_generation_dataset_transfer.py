import pandas as pd
import json
import re
from config import BASE_DIR

# 读取CSV文件
csv_path = f"{BASE_DIR}/Data/DTS-data/training/filtered_finetuning_dataset.csv"  # 请替换为实际的CSV文件路径
data = pd.read_csv(csv_path)

# 存储生成的JSON数据
output_data = []

# 遍历CSV中的每一行数据
for index, row in data.iterrows():
    # 定义 instruction
    instruction = "Generate an SQL query based on the given filtered database schema and its samplings."

    # 去除多余空格，并确保引号转换整洁
    question = row['question'].replace('""', '"')
    filtered_schema = re.sub(r'\s+', ' ', row['filtered_database_schema']).replace('\"', '"')
    query = row['query'].strip()  # 去除可能的首尾空格

    # 定义input和output字段
    input_text = f"###question: {question} ###filtered_database_schema: {filtered_schema}"
    output_text = query

    # 创建一个字典结构用于存储该条数据
    entry = {
        "instruction": instruction,
        "input": input_text,
        "output": output_text
    }

    # 将该条数据添加到输出数据列表中
    output_data.append(entry)

# 将结果保存为JSON文件
json_path = f"{BASE_DIR}/Training_Dataset/DTS/dts_sql_generation_DDLform.json"  # 输出文件路径
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=4)

print(f"DDL风格的sql生成微调JSON数据集已保存至 {json_path}")
