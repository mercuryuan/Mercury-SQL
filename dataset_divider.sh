#!/bin/bash

# 定义JSON和SQL文件路径
bird_json_file="Data/BIRD/output_prompts.json"
bird_sql_file="Data/BIRD/train_gold.sql"
spider_csv_file="Data/DTS-data/training/filtered_finetuning_dataset.csv"

## 生成spider训练集
#python Dataset_Tools/divider/divider.py --spider_csv="$spider_csv_file" --percentage=20 --mode=spider
#python Dataset_Tools/divider/divider.py --spider_csv="$spider_csv_file" --percentage=40 --mode=spider
#python Dataset_Tools/divider/divider.py --spider_csv="$spider_csv_file" --percentage=60 --mode=spider
#python Dataset_Tools/divider/divider.py --spider_csv="$spider_csv_file" --percentage=80 --mode=spider
#python Dataset_Tools/divider/divider.py --spider_csv="$spider_csv_file" --percentage=100 --mode=spider
## 调用divider.py并生成不同的BIRD训练集
#python Dataset_Tools/divider/divider.py --json_file="$bird_json_file" --sql_file="$bird_sql_file" --percentage=20 --mode=bird
#python Dataset_Tools/divider/divider.py --json_file="$bird_json_file" --sql_file="$bird_sql_file" --percentage=40 --mode=bird
#python Dataset_Tools/divider/divider.py --json_file="$bird_json_file" --sql_file="$bird_sql_file" --percentage=60 --mode=bird
#python Dataset_Tools/divider/divider.py --json_file="$bird_json_file" --sql_file="$bird_sql_file" --percentage=80 --mode=bird
#python Dataset_Tools/divider/divider.py --json_file="$bird_json_file" --sql_file="$bird_sql_file" --percentage=100 --mode=bird
#生成Bird的eval数据集
python Dataset_Tools/divider/eval_dataset_creator.py --mode bird --json_file $bird_json_file --sql_file $bird_sql_file --eval
#生成SPIDER的eval数据集
python Dataset_Tools/divider/eval_dataset_creator.py --mode spider --spider_csv $spider_csv_file  --eval


