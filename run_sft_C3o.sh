cd LLaMA-Factory
export CUDA_VISIBLE_DEVICES=0  # 指定只用 GPU 0ni

# 使用指定的配置文件启动训练，并重定义 output_dir
llamafactory-cli train config/sft_Llama3B/C3_orig_train_1_hop_lr_5.yaml
llamafactory-cli train config/sft_Llama3B/C3_orig_train_1_hop_lr_55.yaml
llamafactory-cli train config/sft_Llama3B/C3_train_1_hop.yaml
llamafactory-cli train config/sft_Llama3B/DTS_train_1of2_hop.yaml
llamafactory-cli train config/sft_Llama3B/DTS_train_2of2_hop.yaml