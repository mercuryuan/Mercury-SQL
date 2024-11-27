#!/bin/bash

#                                               !!!!  设置要处理的母文件夹路径  !!!!!
prediction_path=Results/prediction/lr_sft/llama3B/spider
#prediction_path=Results/prediction/2_stage/DTS-8B
#prediction_path=Results/prediction/2_stage/DTS

# 运行生成 SQL 查询的脚本并捕获输出
output=$(python Results/process_predictions.py $prediction_path)

# 提取每一行的预测文件路径并逐个运行 Evaluation/evaluation.py
while IFS= read -r line; do
    # 使用正则表达式提取 predict.txt 文件的路径
    if [[ $line =~ ${prediction_path//\//\\/}/[a-zA-Z0-9_-]+/predict.txt ]]; then
        pred_file="${BASH_REMATCH[0]}"

        # 定义其他参数
        gold="Datasets/spider/dev_gold.sql"
        eval_type="all"
        db="Datasets/spider/database"
        table="Datasets/spider/tables.json"

        # 调用 evaluation.py 并传递参数
        python Evaluation/evaluation.py \
            --gold "$gold" \
            --etype "$eval_type" \
            --db "$db" \
            --table "$table" \
            --pred "$pred_file"
    fi
done <<< "$output"
