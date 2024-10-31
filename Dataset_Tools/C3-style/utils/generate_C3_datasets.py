import json
import argparse
import os.path


def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def merge_datasets(questions_file, schema_file, output_file):
    questions_data = read_json_file(questions_file)
    schema_data = read_json_file(schema_file)
    merged_data = []

    for i in range(len(questions_data)):
        question = questions_data[i]
        schema = schema_data[i]

        # 构建合并项
        input_data = {
            'question': question['question'],
            'db_id': question['db_id'],
            'db_schema': {
                'foreign key': [
                    f"{item['source_table_name_original']}.{item['source_column_name_original']}->{item['target_table_name_original']}.{item['target_column_name_original']}"
                    for item in schema['fk']
                ],
                'primary key': [
                    f"{item['table_name_original']}.{item['column_name_original']}"
                    for item in schema['pk']
                ],
                'tables': [
                    f"{table['table_name']}({', '.join(table['column_names'])})"
                    for table in schema['db_schema']
                ]
            }
        }

        # 转换为所需的字符串格式
        input_str = f"###question:{input_data['question']}, ###db_name: '{input_data['db_id']}',###database_schema: {json.dumps(input_data['db_schema'])}"

        merged_item = {
            'instruction': "###Generate an SQL query based on the provided question and database schema.",
            'input': input_str,
            'output': question['query']
        }

        merged_data.append(merged_item)

    # 写入输出文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(merged_data, file, indent=4)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Merge two JSON datasets with unique IDs.")
    parser.add_argument('--questions_file', required=True, help="Path to the questions JSON file")
    parser.add_argument('--schema_file', required=True, help="Path to the schema JSON file")
    parser.add_argument('--output_file', required=True, help="Path to the output JSON file")
    args = parser.parse_args()
    merge_datasets(args.questions_file, args.schema_file, args.output_file)
