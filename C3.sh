#!/bin/bash
set -e

# 获取项目根目录
PROJECT_ROOT=$(pwd)

# 创建 generate_schema 目录
#if [ ! -d "$PROJECT_ROOT/generate_schema" ]; then
#  mkdir "$PROJECT_ROOT/generate_schema"
#  echo "create directory generate_schema"
#else
#  echo "directory generate_schema already exists"
#fi

# preprocess schema
echo "preprocessing ..."
# 调用预处理脚本
python "$PROJECT_ROOT/Dataset_Tools/C3-style/generate_C3_schema.py" \
    --mode "test" \
    --table_path "$PROJECT_ROOT/Datasets/spider/tables.json" \
    --input_dataset_path "$PROJECT_ROOT/Datasets/spider/train_spider.json" \
    --output_dataset_path "$PROJECT_ROOT/Data/C3-data/train_schema_C3form.json" \
    --db_path "$PROJECT_ROOT/Datasets/spider/database" \
    --target_type "sql"
echo "train数据库模式已保存至：$PROJECT_ROOT/Data/C3-data/train_schema_C3form.json"
python "$PROJECT_ROOT/Dataset_Tools/C3-style/generate_C3_schema.py" \
    --mode "test" \
    --table_path "$PROJECT_ROOT/Datasets/spider/tables.json" \
    --input_dataset_path "$PROJECT_ROOT/Datasets/spider/train_dev.json" \
    --output_dataset_path "$PROJECT_ROOT/Data/C3-data/dev_schema_C3form.json" \
    --db_path "$PROJECT_ROOT/Datasets/spider/database" \
    --target_type "sql"
echo "dev数据库模式已保存至：$PROJECT_ROOT/Data/C3-data/dev_schema_C3form.json"