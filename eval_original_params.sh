# 本脚本是为了测试default脚本与llama脚本的差异
# 结论是llama脚本比默认性能提高

gold=Datasets/spider/dev_gold.sql
eval_type=all
db=Datasets/spider/database
table=Datasets/spider/tables.json

python Evaluation/evaluation.py   \
 --gold $gold \
 --etype $eval_type \
 --db $db \
 --table $table\
 --pred Results/prediction/tp_llama/C3o_lr5/predict.txt

# --pred Results/prediction/tp_llama/C3o_lr5/predict.txt
# --pred Results/prediction/tp_llama/C3o_lr7/predict.txt
# --pred Results/prediction/tp_llama/C3/predict.txt


