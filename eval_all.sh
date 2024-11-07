# 本脚本  用于一切评估
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
 --pred Results/prediction/temperature/06/predict.txt

# --pred Results/prediction/tp_llama/C3o_lr5/predict.txt
# --pred Results/prediction/tp_llama/C3o_lr7/predict.txt
# --pred Results/prediction/tp_llama/C3/predict.txt
# --pred Results/prediction/lr_5-vs_008/lowest_train_loss/predict.txt
# --pred Results/prediction/lr_5-vs_008/lowest_eval_loss/predict.txt
# --pred Results/prediction/temperature/02/predict.txt
# --pred Results/prediction/temperature/06/predict.txt


