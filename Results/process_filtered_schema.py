import os
import json
import argparse


def extract_and_combine(input_filename, output_filename):
    """
    从 JSONL 文件中提取 question 和 predict 字段，格式化为指定的 JSON 输出并写入到输出文件。
    """
    try:
        with open(input_filename, 'r', encoding='UTF-8') as file:
            # 初始化一个空列表来存储所有格式化后的记录
            formatted_records = []

            # 逐行读取文件
            for line in file:
                # 将 JSON 字符串解析为 Python 字典
                data = json.loads(line)

                # 提取 question 和 predict 字段并进行格式化
                if 'question' in data['prompt'] and 'predict' in data:
                    # 提取 question 内容
                    question_part = data['prompt'].split('###question: ')[1].split(',###')[0].strip()

                    # 提取 schema 内容
                    schema_part = data['prompt'].split('###full_database_schema: ')[1].split(', assistant')[0].strip()

                    # 构造目标格式的 JSON 记录
                    record = {
                        "instruction": "Generate an SQL query based on the question and filtered schema. The output should be a single SQL statement.",
                        "input": f"###question: {question_part}, ###filtered schema: {schema_part}",
                        "output": ""
                    }

                    # 添加到记录列表中
                    formatted_records.append(record)

        # 将格式化后的记录写入 JSON 文件
        with open(output_filename, 'w', encoding='UTF-8') as output_file:
            json.dump(formatted_records, output_file, ensure_ascii=False, indent=4)

        print(f"格式化后的 JSON 数据已保存至 {output_filename}")

    except FileNotFoundError:
        print(f"文件 {input_filename} 未找到。")
    except json.JSONDecodeError:
        print(f"文件 {input_filename} 中的 JSON 解码错误。")
    except Exception as e:
        print(f"发生错误: {e}")


def process_all_subfolders(base_dir):
    """
    遍历给定文件夹下的所有子文件夹，并对其中的 generated_predictions.jsonl 文件执行提取操作。
    """
    for root, dirs, files in os.walk(base_dir):
        for subdir in dirs:
            input_file = os.path.join(base_dir, subdir, "generated_predictions.jsonl")
            output_file = os.path.join(base_dir, subdir, "filtered_schema.json")

            # 如果文件存在，执行提取和格式化操作
            if os.path.isfile(input_file):
                extract_and_combine(input_file, output_file)


if __name__ == "__main__":
    # 使用 argparse 解析命令行参数
    parser = argparse.ArgumentParser(
        description="Extract question and predict fields, format as JSON, and save to output file.")
    parser.add_argument("base_dir", type=str,
                        help="The base directory containing subfolders with generated_predictions.jsonl files.")
    args = parser.parse_args()

    # 运行主处理函数
    process_all_subfolders(args.base_dir)
