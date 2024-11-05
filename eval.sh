 检查目录是否存在
pwd
ls

 检查文件是否存在
test -f Datasets/spider/dev_gold.sql && echo "dev_gold.sql exists" || echo "dev_gold.sql does not exist"
test -f result/predict.txt && echo "predict.txt exists" || echo "predict.txt does not exist"
test -d Datasets/spider/database && echo "database exists" || echo "database does not exist"  # 注意：这里假设database是一个文件，如果它是目录，请使用 test -d
test -f Datasets/spider/tables.json && echo "tables.json exists" || echo "tables.json does not exist"

python third_party/evaluation.py --gold spider/dev_gold.sql --pred result/predict.txt --etype all --db spider/database --table spider/tables.json