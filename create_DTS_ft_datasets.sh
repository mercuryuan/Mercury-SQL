
export PYTHONPATH="F:/Mercury-SQL:$PYTHONPATH"  # 设置 PYTHONPATH

python Dataset_Tools/DTS-style/finetuning_dataset_creator.py
echo "DTS-style数据集构造完成"

python Dataset_Tools/DTS-style/dts_schema_linking_dataset_transfer.py
echo "schema linking阶段微调prompt构造完成"

python Dataset_Tools/DTS-style/dts_sql_generation_dataset_transfer.py
echo "sql generation阶段微调prompt构造完成"
