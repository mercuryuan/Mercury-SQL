import json
import re
import pandas as pd
import argparse


def generate_eval_dataset_from_bird(json_file, sql_file):
    """
    直接处理完整的BIRD JSON文件，生成评估数据集（output置为空）。

    :param json_file: 原始JSON文件路径
    :param sql_file: 对应SQL文件路径，用于校验条目数一致性
    """
    # 读取JSON文件
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 读取SQL文件
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_queries = f.readlines()

    # 校验SQL数量是否与JSON条目一致
    if len(data) != len(sql_queries):
        raise ValueError("JSON条目数与SQL查询数不一致，请检查输入文件！")

    # 格式化数据，output置为空
    formatted_data = [
        {
            "instruction": "",
            "input": f"-- question: {entry['question']} -- db_name: {entry['db_id']} -- schema: {entry['schema']} {entry['external knowledge']}Generate the SQL after thinking step by step: \nSELECT ",
            "output": ""  # output置为空
        }
        for entry in data
    ]

    # 输出文件名
    output_file = "Training_Dataset/Divided/BIRD_eval_full.json"

    # 写入新JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, ensure_ascii=False, indent=4)

    print(f"完整评估数据集生成完成，文件：{output_file}，包含 {len(formatted_data)} 条记录。")


def generate_eval_dataset_from_spider(csv_path):
    """
    直接处理完整的Spider CSV文件，生成评估数据集（output内容为空）。

    :param csv_path: 输入的CSV文件路径
    """
    # 读取CSV数据
    data = pd.read_csv(csv_path)

    # 存储生成的JSON数据
    output_data = []

    # 遍历数据
    for index, row in data.iterrows():
        # 定义 instruction
        instruction = "Generate an SQL query based on the given question, database schema and its samplings."

        # 去除多余空格，并确保引号转换整洁
        question = row['question'].replace('""', '"')
        filtered_schema = re.sub(r'\s+', ' ', row['database_schema']).replace('\"', '"')

        # 定义 input 和 output 字段
        input_text = f"###question: {question} ###filtered_database_schema: {filtered_schema}"
        output_text = ""  # output 置为空

        # 创建一个字典结构用于存储该条数据
        entry = {
            "instruction": instruction,
            "input": input_text,
            "output": output_text
        }

        # 将该条数据添加到输出数据列表中
        output_data.append(entry)

    # 定义输出JSON路径
    output_file = "Training_Dataset/Divided/SPIDER_eval_full.json"

    # 将结果保存为JSON文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"完整评估数据集生成完成，文件：{output_file}，包含 {len(output_data)} 条记录。")


def main():
    # 创建参数解析器
    parser = argparse.ArgumentParser(description="生成完整数据集或评估数据集")
    parser.add_argument("--mode", type=str, choices=["bird", "spider"], required=True,
                        help="选择运行模式：bird 或 spider")
    parser.add_argument("--json_file", type=str, help="输入的BIRD的JSON文件路径")
    parser.add_argument("--sql_file", type=str, help="输入的SQL文件路径")
    parser.add_argument("--spider_csv", type=str, help="输入的Spider的CSV文件路径")
    parser.add_argument("--eval", action="store_true", help="是否生成评估数据集，默认生成训练数据")

    # 解析参数
    args = parser.parse_args()

    # 根据模式调用对应的函数
    if args.mode == "bird":
        if not args.json_file or not args.sql_file:
            raise ValueError("在 bird 模式下，必须提供 --json_file 和 --sql_file 参数")
        generate_eval_dataset_from_bird(args.json_file, args.sql_file)
    elif args.mode == "spider":
        if not args.spider_csv:
            raise ValueError("在 spider 模式下，必须提供 --spider_csv 参数")
        generate_eval_dataset_from_spider(args.spider_csv)


if __name__ == "__main__":
    main()
