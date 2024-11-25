import json
import random
import argparse
import re

import pandas as pd


def extract_sample_with_sql_in_bird(json_file, sql_file, percentage):
    """
    抽取百分之几的JSON条目作为微调数据，同时引入对应的SQL查询作为output，并输出为新的JSON文件。

    :param json_file: 原始JSON文件路径
    :param sql_file: 对应SQL文件路径，每行SQL对应一个JSON条目的结果
    :param percentage: 抽样比例（0-100）
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

    # 计算抽样数量
    sample_size = max(1, int(len(data) * (percentage / 100)))

    # 随机抽取样本
    sampled_indices = random.sample(range(len(data)), sample_size)

    # 重新格式化数据，并将SQL作为output
    formatted_data = [
        {
            "instruction": "",
            "input": f"-- question: {data[i]['question']} -- schema: {data[i]['schema']} {data[i]['external knowledge']}Generate the SQL after thinking step by step: \nSELECT ",
            "output": sql_queries[i].strip()  # 对应的SQL查询，去掉行尾换行符
        }
        for i in sampled_indices
    ]

    # 输出文件名
    output_file = f"Training_Dataset/Divided/BIRD_train_{int(percentage)}%.json"
    # 写入新JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(formatted_data, f, ensure_ascii=False, indent=4)

    print(f"抽样完成，生成文件：{output_file}，包含 {len(formatted_data)} 条记录。")


def extract_sample_with_sql_in_spider(csv_path, percentage):
    """
    从CSV文件中按比例抽取数据，并生成微调所需的JSON格式数据。

    :param csv_path: 输入的CSV文件路径
    :param percentage: 抽样比例（0-100）
    """
    # 读取CSV数据
    data = pd.read_csv(csv_path)

    # 校验比例范围
    if not (0 < percentage <= 100):
        raise ValueError("percentage 应该在 (0, 100] 范围内")

    # 计算抽样数量
    sample_size = max(1, int(len(data) * (percentage / 100)))

    # 随机抽取样本
    sampled_indices = random.sample(range(len(data)), sample_size)
    sampled_data = data.iloc[sampled_indices]

    # 存储生成的JSON数据
    output_data = []

    # 遍历抽样后的数据
    for index, row in sampled_data.iterrows():
        # 定义 instruction
        instruction = "Generate an SQL query based on the given question,database schema and its samplings."

        # 去除多余空格，并确保引号转换整洁
        question = row['question'].replace('""', '"')
        filtered_schema = re.sub(r'\s+', ' ', row['database_schema']).replace('\"', '"')
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

    # 定义输出JSON路径
    output_file = f"Training_Dataset/Divided/SPIDER_train_{int(percentage)}%.json"

    # 将结果保存为JSON文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"按比例采样完成，生成文件：{output_file}，包含 {len(output_data)} 条记录。")


import argparse


def main():
    # 创建参数解析器
    parser = argparse.ArgumentParser(description="抽取数据并生成新的JSON文件")
    parser.add_argument("--mode", type=str, choices=["bird", "spider"], required=True,
                        help="选择运行模式：bird 或 spider")
    parser.add_argument("--json_file", type=str, help="输入的BIRD的JSON文件路径")
    parser.add_argument("--sql_file", type=str, help="输入的SQL文件路径")
    parser.add_argument("--spider_csv", type=str, help="输入的Spider的CSV文件路径")
    parser.add_argument("--percentage", type=float, required=True, help="抽样比例（0-100）")

    # 解析参数
    args = parser.parse_args()

    # 根据模式调用对应的函数
    if args.mode == "bird":
        if not args.json_file or not args.sql_file:
            raise ValueError("在 bird 模式下，必须提供 --json_file 和 --sql_file 参数")
        extract_sample_with_sql_in_bird(args.json_file, args.sql_file, args.percentage)
    elif args.mode == "spider":
        if not args.spider_csv:
            raise ValueError("在 spider 模式下，必须提供 --spider_csv 参数")
        extract_sample_with_sql_in_spider(args.spider_csv, args.percentage)


if __name__ == "__main__":
    main()
