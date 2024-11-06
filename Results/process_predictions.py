import os
import json
import argparse


def extract_sql_queries(input_filename, output_filename):
    """
    从 JSONL 文件中提取 SQL 查询并将其写入到指定的输出文件中。
    """
    try:
        with open(input_filename, 'r', encoding='UTF-8') as file:
            # 初始化一个空列表来存储所有的SQL查询
            queries = []

            # 读取文件的每一行，假设每行是一个独立的JSON对象
            for line in file:
                # 将JSON字符串解析为Python字典
                data = json.loads(line)

                # 提取predict字段并添加到列表中
                if 'predict' in data:
                    queries.append(data['predict'])

        # 将所有SQL查询写入一个文件
        with open(output_filename, 'w', encoding='UTF-8') as output_file:
            for query in queries:
                # 将每个查询语句写入文件，并在每个查询后添加一个分号和换行符
                output_file.write(query + ';\n')

        print(f"SQL queries 已保存至 {output_filename}")

    except FileNotFoundError:
        print(f"File {input_filename} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file {input_filename}.")
    except Exception as e:
        print(f"An error occurred: {e}")


def process_all_subfolders(base_dir):
    """
    遍历给定文件夹下的所有子文件夹，并对其中的 generated_predictions.jsonl 文件执行提取操作。
    """
    for root, dirs, files in os.walk(base_dir):
        for subdir in dirs:
            input_file = os.path.join(base_dir, subdir, "generated_predictions.jsonl")
            output_file = os.path.join(base_dir, subdir, "predict.txt")

            # 如果文件存在，执行提取SQL查询的操作
            if os.path.isfile(input_file):
                print(f"处理模型预测文件: {input_file}")
                extract_sql_queries(input_file, output_file)


if __name__ == "__main__":
    # 使用 argparse 解析命令行参数
    parser = argparse.ArgumentParser(
        description="Extract SQL queries from generated_predictions.jsonl files in each subfolder.")
    parser.add_argument("base_dir", type=str,
                        help="The base directory containing subfolders with generated_predictions.jsonl files.")
    args = parser.parse_args()

    # 运行主处理函数
    process_all_subfolders(args.base_dir)
