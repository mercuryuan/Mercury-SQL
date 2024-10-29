
export PYTHONPATH="F:/Mercury-SQL:$PYTHONPATH"  # 设置 PYTHONPATH
echo "构造spider微调数据集"
python Dataset_Tools/DTS-style/finetuning_dataset_creator.py
echo "DTS-style数据集构造完成"
echo "转化为DDL风格的prompt微调数据集"
python Dataset_Tools/DTS-style/dts_schema_linking_dataset_transfer.py
echo "schema linking阶段微调数据集构造完成"
python Dataset_Tools/DTS-style/dts_sql_generation_dataset_transfer.py
echo "sql generation阶段微调数据集构造完成"
