#!/bin/bash
set -e

# 获取项目根目录
PROJECT_ROOT=$(pwd)

## 创建 generate_schema 目录
#if [ ! -d "$PROJECT_ROOT/Data/C3-data/" ]; then
#  mkdir "$PROJECT_ROOT/Data/C3-data/"
#  echo "create directory Data/C3-data"
#else
#  echo "directory Data/C3-data already exists"
#fi
#
## preprocess schema
#echo "preprocessing ..."
## 调用预处理脚本
#python "$PROJECT_ROOT/Dataset_Tools/C3-style/generate_C3_schema.py" \
#    --mode "test" \
#    --table_path "$PROJECT_ROOT/Datasets/spider/tables.json" \
#    --input_dataset_path "$PROJECT_ROOT/Datasets/spider/train_spider.json" \
#    --output_dataset_path "$PROJECT_ROOT/Data/C3-data/train_schema_C3form.json" \
#    --db_path "$PROJECT_ROOT/Datasets/spider/database" \
#    --target_type "sql"
#echo "train数据库模式已保存至：$PROJECT_ROOT/Data/C3-data/train_schema_C3form.json"
#python "$PROJECT_ROOT/Dataset_Tools/C3-style/generate_C3_schema.py" \
#    --mode "test" \
#    --table_path "$PROJECT_ROOT/Datasets/spider/tables.json" \
#    --input_dataset_path "$PROJECT_ROOT/Datasets/spider/dev.json" \
#    --output_dataset_path "$PROJECT_ROOT/Data/C3-data/dev_schema_C3form.json" \
#    --db_path "$PROJECT_ROOT/Datasets/spider/database" \
#    --target_type "sql"
#echo "dev数据库模式已保存至：$PROJECT_ROOT/Data/C3-data/dev_schema_C3form.json"
echo  "生成C3微调数据集"
python $PROJECT_ROOT/Dataset_Tools/C3-style/utils/generate_C3_datasets.py  --questions_file "$PROJECT_ROOT\Datasets\spider\train_spider.json" --schema_file "$PROJECT_ROOT\Data\C3-data\train_schema_C3form.json" --output_file "$PROJECT_ROOT/Training_Dataset/C3/train.json"
python $PROJECT_ROOT/Dataset_Tools/C3-style/utils/generate_C3_datasets.py  --questions_file "$PROJECT_ROOT\Datasets\spider\dev.json" --schema_file "$PROJECT_ROOT\Data\C3-data\dev_schema_C3form.json" --output_file "$PROJECT_ROOT/Training_Dataset/C3/dev.json"
echo "schema信息已导出至：$PROJECT_ROOT/Training_Dataset/C3"


