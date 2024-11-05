#!/bin/bash

# 进入 LLaMA-Factory 目录
cd LLaMA-Factory

# 设置模型名称和当前日期
MODEL_NAME="llama3B"
current_date=$(date +%F)

# 创建以当前日期命名的文件夹
if [ ! -d "Results/$current_date/$MODEL_NAME" ]; then
    mkdir -p "Results/$current_date/$MODEL_NAME"
    echo "文件夹 'Results/$current_date/$MODEL_NAME' 已创建。"
else
    echo "文件夹 'Results/$current_date/$MODEL_NAME' 已存在。"
fi

# 定义训练命令和对应的日志文件名称
commands=(
    "llamafactory-cli train config/sft_Llama3B/f32/C3_orig_train_1_hop_lr_5.yaml"
    "llamafactory-cli train config/sft_Llama3B/f32/C3_orig_train_1_hop_lr_55.yaml"
    "llamafactory-cli train config/sft_Llama3B/f32/C3_train_1_hop.yaml"
    "llamafactory-cli train config/sft_Llama3B/f32/DTS_train_1of2_hop.yaml"
    "llamafactory-cli train config/sft_Llama3B/f32/DTS_train_2of2_hop.yaml"
)

# 对应的日志文件名称
log_files=(
    "C3_orig_train_1_hop_lr_5.txt"
    "C3_orig_train_1_hop_lr_55.log"
    "C3_train_1_hop.txt"
    "DTS_train_1of2_hop.txt"
    "DTS_train_2of2_hop.txt"
)

# 定义每个命令使用的 GPU
gpu_assignments=(0 0 1 2 2)  # 例如，第一个和第二个任务使用 GPU 0，第三个任务使用 GPU 1，第四和第五个任务使用 GPU 2

# 循环启动每个训练任务
for i in "${!commands[@]}"; do
    # 获取对应的日志文件路径
    log_file="Results/$current_date/$MODEL_NAME/${log_files[$i]}"

    # 使用 tee 命令同时输出到终端和日志文件
    CUDA_VISIBLE_DEVICES=${gpu_assignments[$i]} eval "${commands[$i]} 2>&1 | tee $log_file" &  # 指定 GPU
done

# 等待所有后台任务完成
wait
echo "所有训练任务已完成。"
