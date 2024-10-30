import json


# 读取 JSON 文件
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


# 合并数据集并添加 id
def merge_datasets(questions_file, schema_file, output_file):
    questions_data = read_json_file(questions_file)
    schema_data = read_json_file(schema_file)

    # 初始化结果列表
    merged_data = []

    # 遍历 questions_data 和 schema_data，假设它们的长度相同且顺序一一对应
    for i in range(len(questions_data)):
        question = questions_data[i]
        schema = schema_data[i]

        # 提取所需的字段
        merged_item = {
            'id': i + 1,  # 为每一条记录添加一个唯一的 id
            'question': question['question'],
            'db_id': question['db_id'],
            'query': question['query'],
            'db_schema': {
                'fk': schema['fk'],
                'pk': schema['pk'],
                'tables': [
                    {
                        'table_name': table['table_name'],
                        'column_names': table['column_names']
                    } for table in schema['db_schema']
                ]
            }
        }

        # 添加到结果列表
        merged_data.append(merged_item)

    # 将合并后的数据写入新的 JSON 文件
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(merged_data, file, indent=4)


# 指定 JSON 文件路径
questions_file_path = '../data/spider/train_spider.json'
schema_file_path = '../generate_schema/output_schema.json'
output_file_path = '../my_dataset/raw_input_output.json'

# 执行合并
merge_datasets(questions_file_path, schema_file_path, output_file_path)
