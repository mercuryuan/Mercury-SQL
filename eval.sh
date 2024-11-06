gold=Datasets/spider/dev_gold.sql
eval_type=all
db=Datasets/spider/database
table=Datasets/spider/tables.json

python Evaluation/evaluation.py   \
 --gold $gold \
 --etype $eval_type \
 --db $db \
 --table $table\
 --pred Results/prediction/tp_default/C3o_lr5/predict.txt

