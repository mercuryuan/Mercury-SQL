db_root_path='Datasets/BIRD_dev/dev_databases/'
data_mode='dev'
diff_json_path='Datasets/BIRD_dev/dev.json'
#predicted_sql_path='./exp_result/turbo_output/'
ground_truth_path='Datasets/BIRD_dev/'
num_cpus=16
meta_time_out=30.0
mode_gt='gt'
mode_predict='gpt'

# 手动配置
#predicted_sql_path_kg=Results/prediction/lr_sft/llama1B/bird/100/
#predicted_sql_path_kg=Results/prediction/lr_sft/llama1B/bird/80/
#predicted_sql_path_kg=Results/prediction/lr_sft/llama1B/bird/60/
#predicted_sql_path_kg=Results/prediction/lr_sft/llama1B/bird/40/
predicted_sql_path_kg=Results/prediction/lr_sft/llama1B/bird/20/
#predicted_sql_path_kg=Results/prediction/lr_sft/llama3B/bird/100/
#predicted_sql_path_kg='Results/prediction/lr_sft/llama3B/bird/20/'
#predicted_sql_path_kg='Results/prediction/lr_sft/llama3B/bird/40/'
#predicted_sql_path_kg=Results/prediction/lr_sft/llama3B/bird/60/
#predicted_sql_path_kg=Results/prediction/lr_sft/llama3B/bird/80/


echo '''starting to compare with knowledge for ex'''
python -u Evaluation/evaluation_bird/evaluation.py --db_root_path ${db_root_path} --predicted_sql_path ${predicted_sql_path_kg} --data_mode ${data_mode} \
--ground_truth_path ${ground_truth_path} --num_cpus ${num_cpus} --mode_gt ${mode_gt} --mode_predict ${mode_predict} \
--diff_json_path ${diff_json_path} --meta_time_out ${meta_time_out}

#echo '''starting to compare without knowledge for ex'''
#python -u ./src/evaluation.py --db_root_path ${db_root_path} --predicted_sql_path ${predicted_sql_path} --data_mode ${data_mode} \
#--ground_truth_path ${ground_truth_path} --num_cpus ${num_cpus} --mode_gt ${mode_gt} --mode_predict ${mode_predict} \
#--diff_json_path ${diff_json_path} --meta_time_out ${meta_time_out}

echo '''starting to compare with knowledge for ves'''
python -u Evaluation/evaluation_bird/evaluation_ves.py --db_root_path ${db_root_path} --predicted_sql_path ${predicted_sql_path_kg} --data_mode ${data_mode} \
--ground_truth_path ${ground_truth_path} --num_cpus ${num_cpus} --mode_gt ${mode_gt} --mode_predict ${mode_predict} \
--diff_json_path ${diff_json_path} --meta_time_out ${meta_time_out}

#echo '''starting to compare without knowledge for ves'''
#python -u ./src/evaluation_ves.py --db_root_path ${db_root_path} --predicted_sql_path ${predicted_sql_path} --data_mode ${data_mode} \
#--ground_truth_path ${ground_truth_path} --num_cpus ${num_cpus} --mode_gt ${mode_gt} --mode_predict ${mode_predict} \
#--diff_json_path ${diff_json_path} --meta_time_out ${meta_time_out}