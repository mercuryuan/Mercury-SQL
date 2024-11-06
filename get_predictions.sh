# 该脚本实现将输入dir中的子文件夹中的generated_predictions.jsonl
# 写入原目录下的predict.txt中
python Results/process_predictions.py Results/prediction/tp_default
python Results/process_predictions.py Results/prediction/tp_llama