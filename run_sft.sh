cd LLaMA-Factory
export CUDA_VISIBLE_DEVICES=0  # 指定只用 GPU 0ni

# 使用指定的配置文件启动训练，并重定义 output_dir
llamafactory-cli train config/sft/llama3B_sft_bz_2.yaml
#llamafactory-cli train config/sft/llama3_sft_bz_2.yaml

