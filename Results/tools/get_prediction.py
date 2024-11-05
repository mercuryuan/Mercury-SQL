import json

# 假设你的JSON记录存储在同一个文件中，这里我们称之为 data.json
input_filename = '../prediction/C3_orig_eval_1_hop/generated_predictions.jsonl'
output_filename = '../prediction/C3_orig_eval_1_hop/sql_queries.txt'

# 打开输入文件并读取数据
with open(input_filename, 'r', encoding='UTF-8') as file:
    # 初始化一个空列表来存储所有的SQL查询
    queries = []

    # 读取文件的每一行，假设每行是一个独立的JSON对象
    for line in file:
        # 将JSON字符串解析为Python字典
        data = json.loads(line)

        # 提取predict字段并添加到列表中
        queries.append(data['predict'])

# 将所有SQL查询写入一个文件
with open(output_filename, 'w', encoding='UTF-8') as output_file:
    for query in queries:
        # 将每个查询语句写入文件，并在每个查询后添加一个分号和换行符
        output_file.write(query + ';\n')

print(f"SQL queries have been written to {output_filename}")
