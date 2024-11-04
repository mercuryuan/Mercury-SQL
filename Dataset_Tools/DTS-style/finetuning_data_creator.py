import pandas as pd
import os
from tqdm import tqdm
from utils.database_formatter import get_table_schema_with_samples, get_all_table_names
from utils.sql_regularizator import format_and_lowercase_sql_query
from utils.prompts import (
    sql_generation_prompt_token_counter,
    schema_linking_prompt_token_counter,
)
from transformers import AutoTokenizer
from sql_metadata import Parser
from config import BASE_DIR, SPIDER_DATA_PATH

# 模型名或者本地路径
MODEL_NAME = "meta-llama/Llama-3.2-1B"
# MODEL_NAME = "meta-llama/Llama-3.2-3B"

CONTEXT_WINDOW = 3000

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
# 要设置聊天模板，否则报错
chat_template = """{%- for message in messages %}
    {{- '<|im_start|>' + message['role'] + '\n' + message['content'] + '<|im_end|>' + '\n' }}
{%- endfor %}
"""
tokenizer.chat_template = chat_template
print(tokenizer.chat_template)  # 输出目前应用的模板


def load_spider_train_set():
    # 读取train_others.json文件
    df1 = pd.read_json(os.path.join(BASE_DIR, "Datasets/spider/train_others.json"))
    # 读取train_spider.json文件
    df2 = pd.read_json(os.path.join(BASE_DIR, "Datasets/spider/train_spider.json"))
    # 将df1和df2合并为一个DataFrame
    df = pd.concat([df1, df2])
    # 重置索引并删除旧的索引列
    df = df.reset_index(drop=True)
    # 返回合并后的DataFrame
    return df


def load_spider_dev_set():
    # 读取开发集数据
    df = pd.read_json(os.path.join(BASE_DIR, "Datasets/spider/dev.json"))
    # 返回读取的数据框
    return df


def create_sql_generation_correct_tables(dataset, question, query, db_uri):
    # 解析SQL查询中的正确表名
    correct_tables = Parser(query).tables
    # 解析SQL查询中的正确列名
    correct_columns = Parser(query).columns
    # 初始化过滤后的数据库模式为空字符串
    database_schema_filtered = ""
    # 遍历正确的表名，获取每个表的模式并添加到过滤后的数据库模式中
    for table in correct_tables:
        database_schema_filtered += get_table_schema_with_samples(db_uri, table)
        database_schema_filtered += "\n"

    # 初始化完整的数据库模式为空字符串
    database_schema = ""
    # 获取数据库中所有表名
    all_tables = get_all_table_names(db_uri)
    # 遍历所有表名，获取每个表的模式并添加到完整的数据库模式中
    for table in all_tables:
        database_schema += get_table_schema_with_samples(db_uri, table)
        database_schema += "\n"

    # 检查问题、过滤后的数据库模式、正确的表名和列名是否在上下文窗口大小内
    if (
            schema_linking_prompt_token_counter(question, database_schema, correct_tables, correct_columns, tokenizer)
            <= CONTEXT_WINDOW
    ):
        # 如果在上下文窗口大小内，将相关信息添加到数据集中
        dataset.append(
            {
                "db_id": db_uri.split("/")[-1].split(".")[0],  # 获取数据库ID
                "question": question,  # 问题文本
                "query": query,  # SQL查询
                "filtered_database_schema": database_schema_filtered,  # 过滤后的数据库模式
                "database_schema": database_schema,  # 完整的数据库模式
                "correct_tables": ", ".join(correct_tables),  # 正确的表名，用逗号分隔
                "correct_columns": ", ".join(correct_columns),  # 正确的列名，用逗号分隔
            }
        )
    return dataset


def create_full_sql_generation(
        dataset, question, query, db_uri, full_finetuning_errors
):
    # 初始化数据库模式字符串
    database_schema = ""
    # 获取所有表名
    all_tables = get_all_table_names(db_uri)
    # 遍历所有表名
    for table in all_tables:
        # 获取表模式并追加到数据库模式字符串中
        database_schema += get_table_schema_with_samples(db_uri, table)
        # 在数据库模式字符串末尾添加换行符
        database_schema += "\n"
    # 判断问题、数据库模式和查询是否满足上下文窗口大小限制
    if (
            sql_generation_prompt_token_counter(question, database_schema, query, tokenizer)
            <= CONTEXT_WINDOW
    ):
        # 将满足条件的数据添加到数据集中
        dataset.append(
            {
                # 数据库ID
                "db_id": db_uri.split("/")[-1].split(".")[0],
                # 问题
                "question": question,
                # SQL查询
                "query": query,
                # 数据库模式
                "database_schema": database_schema,
            }
        )
    else:
        # 如果不满足上下文窗口大小限制，则错误计数加1
        full_finetuning_errors += 1
    # 返回更新后的数据集和错误计数
    return dataset, full_finetuning_errors


if __name__ == "__main__":
    # 加载Spider训练集
    # Load Spider train set
    df = load_spider_train_set()
    df = df.sample(frac=1).reset_index(drop=True)
    finetuning_dataset = []
    filtered_finetuning_dataset = []
    full_finetuning_errors = 0
    filtered_finetuning_errors = 0
    for index, row in tqdm(df.iterrows(), total=len(df)):
        db_id = row["db_id"]
        question = row["question"]
        query = row["query"]
        # 格式化并转为小写的SQL查询
        query = format_and_lowercase_sql_query(query)
        db_uri = f"{SPIDER_DATA_PATH}/{db_id}/{db_id}.sqlite"
        all_tables = get_all_table_names(db_uri)
        try:
            # 创建使用正确表的SQL生成数据集
            filtered_finetuning_dataset = create_sql_generation_correct_tables(
                filtered_finetuning_dataset, question, query, db_uri
            )
        except Exception:
            filtered_finetuning_errors += 1
        # 创建完整的SQL生成数据集，并更新错误计数
        finetuning_dataset, full_finetuning_errors = create_full_sql_generation(
            finetuning_dataset, question, query, db_uri, full_finetuning_errors
        )
    # 保存微调数据集
    # Save finetuning dataset
    print(f"Full finetuning set errors: {full_finetuning_errors}")
    print(f"Filtered finetuning set errors: {filtered_finetuning_errors}")
    df = pd.DataFrame(finetuning_dataset)
    df.to_csv(os.path.join(BASE_DIR, "Data/DTS-data/training/full_finetuning_dataset.csv"), index=False)
    df = pd.DataFrame(filtered_finetuning_dataset)
    df.to_csv(os.path.join(BASE_DIR, "Data/DTS-data/training/filtered_finetuning_dataset.csv"), index=False)
    # 加载Spider开发集
    # Load Spider dev set
    df = load_spider_dev_set()
    validation_dataset = []
    validation_dataset_fromatted = []
    filtered_validation_dataset = []
    validation_set_errors = 0
    validation_set_formatted_errors = 0
    filtered_validation_set_errors = 0
    for index, row in tqdm(df.iterrows(), total=len(df)):
        db_id = row["db_id"]
        # 使用SpiderSynQuestion字段作为问题
        # question = row["SpiderSynQuestion"]
        question = row["question"]
        query = row["query"]
        # 格式化并转为小写的SQL查询
        formatted_query = format_and_lowercase_sql_query(query)
        db_uri = f"{SPIDER_DATA_PATH}/{db_id}/{db_id}.sqlite"
        try:
            # 创建使用正确表的SQL生成验证数据集
            filtered_validation_dataset = create_sql_generation_correct_tables(
                filtered_validation_dataset, question, formatted_query, db_uri
            )
        except Exception:
            filtered_validation_set_errors += 1
        # 使用格式化查询创建完整的SQL生成验证数据集，并更新格式化错误计数
        validation_dataset_fromatted, validation_set_formatted_errors = create_full_sql_generation(
            validation_dataset_fromatted,
            question,
            formatted_query,
            db_uri,
            validation_set_formatted_errors,
        )
        # 使用原始查询创建完整的SQL生成验证数据集，并更新错误计数
        validation_dataset, validation_set_errors = create_full_sql_generation(
            validation_dataset, question, query, db_uri, validation_set_errors
        )
    print(f"Filtered validation set errors: {filtered_validation_set_errors}")
    print(f"Validation set formatted errors: {validation_set_formatted_errors}")
    print(f"Validation set errors: {validation_set_errors}")
    # 保存验证数据集
    # Save validation dataset
    df = pd.DataFrame(validation_dataset)
    df.to_csv(os.path.join(BASE_DIR, "Data/DTS-data/validation/spider_dataset.csv"), index=False)
    df = pd.DataFrame(validation_dataset_fromatted)
    df.to_csv(os.path.join(BASE_DIR, "Data/DTS-data/validation/spider_dataset_formatted.csv"), index=False)
    df = pd.DataFrame(filtered_validation_dataset)
    df.to_csv(os.path.join(BASE_DIR, "Data/DTS-data/validation/filtered_spider_dataset"), index=False)
