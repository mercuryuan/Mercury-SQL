import os
import json
import argparse


def extract_and_convert_queries(input_filename, output_filename):
    """
    从 JSONL 文件中提取 SQL 查询，并转换为 dev_predict.json 的格式。
    """
    try:
        with open(input_filename, 'r', encoding='UTF-8') as file:
            result = {}
            count = 0  # 用于编号
            for line in file:
                # 将JSON字符串解析为Python字典
                data = json.loads(line)
                if 'predict' in data and data['predict']:
                    # 按目标格式组装每条记录
                    db_name = extract_db_name(data['prompt'])
                    query = f"{data['predict']}\t----- bird -----\t{db_name}"
                    result[str(count)] = query
                    count += 1

        # 将结果写入输出 JSON 文件
        with open(output_filename, 'w', encoding='UTF-8') as output_file:
            json.dump(result, output_file, ensure_ascii=False, indent=4)

        print(f"转换完成，输出文件: {output_filename}")

    except FileNotFoundError:
        print(f"File {input_filename} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file {input_filename}.")
    except Exception as e:
        print(f"An error occurred: {e}")


def process_all_subfolders(base_dir):
    """
    遍历给定文件夹下的所有子文件夹，并对其中的 generated_predictions.jsonl 文件执行提取和转换操作。
    """
    for root, dirs, files in os.walk(base_dir):
        for subdir in dirs:
            input_file = os.path.join(base_dir, subdir, "generated_predictions.jsonl")
            output_file = os.path.join(base_dir, subdir, "dev_predict.json")

            # 如果文件存在，执行提取和转换操作
            if os.path.isfile(input_file):
                # print(f"处理模型预测文件: {input_file}")
                extract_and_convert_queries(input_file, output_file)


def extract_db_name(prompt):
    """
    从 prompt 字段中提取 db_name 的值。
    """
    try:
        start = prompt.find("-- db_name: ")
        if start != -1:
            start += len("-- db_name: ")
            end = prompt.find(" ", start)
            if end == -1:
                end = len(prompt)
            return prompt[start:end]
    except Exception as e:
        print(f"提取数据库名称时发生错误: {e}")
    return None


if __name__ == "__main__":
    # 使用 argparse 解析命令行参数
    parser = argparse.ArgumentParser(
        description="Extract and convert SQL queries to dev_predict.json format.")
    parser.add_argument("base_dir", type=str,
                        help="The base directory containing subfolders with generated_predictions.jsonl files.")
    args = parser.parse_args()

    # 运行主处理函数
    process_all_subfolders(args.base_dir)
