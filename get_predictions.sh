# 该脚本实现将输入dir中的子文件夹中的generated_predictions.jsonl
# 写入原目录下的predict.txt中

# 已运行过的命令
#python Results/process_predictions.py Results/prediction/tp_default
#python Results/process_predictions.py Results/prediction/tp_llama
#python Results/process_predictions.py Results/prediction/tp_llama
#python Results/process_predictions.py Results/prediction/lr_5-vs_008
#python Results/process_predictions.py Results/prediction/temperature
#python Results/process_predictions.py Results/prediction/origin
#python Results/process_predictions.py Results/prediction/2_stage/DTS

# 对于BIRD
python Results/process_predictions_for_bird.py Results/prediction/lr_sft/llama1B/bird
#python Results/process_predictions_for_bird.py Results/prediction/lr_sft/llama3B/bird