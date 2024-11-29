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
fi

# 定义训练命令
commands=(
#    "llamafactory-cli train config/llama3B/lr_inf/spider/20.yaml"
#    "llamafactory-cli train config/llama3B/lr_inf/spider/40.yaml"
#    "llamafactory-cli train config/llama3B/lr_inf/spider/60.yaml"
#    "llamafactory-cli train config/llama3B/lr_inf/spider/80.yaml"
#    "llamafactory-cli train config/llama3B/lr_inf/spider/100.yaml"
#    "llamafactory-cli train config/llama3B/lr_inf/bird/20.yaml"
#    "llamafactory-cli train config/llama3B/lr_inf/bird/40.yaml"
#    "llamafactory-cli train config/llama3B/lr_inf/bird/60.yaml"
#    "llamafactory-cli train config/llama3B/lr_inf/bird/80.yaml"
#    "llamafactory-cli train config/llama3B/lr_inf/bird/100.yaml"
    "llamafactory-cli train config/llama3B/lr_inf/bird/0.yaml"
    "llamafactory-cli train config/llama3B/lr_inf/spider/0.yaml"
)

# 定义可用的 GPU
gpu_count=2  # 可用 GPU 数量
gpu_assignments=(2 3)  # GPU 0 和 GPU 1

# 创建一个空数组来保存当前正在执行的任务的 PID
declare -a running_jobs

# 循环启动每个训练任务
for i in "${!commands[@]}"; do
    # 选择当前可用的 GPU
    gpu_id=${gpu_assignments[$((i % gpu_count))]}  # 循环使用 GPU 0 和 GPU 1

    # 如果这个 GPU 上已经有任务在执行，则等待它完成
    while [[ "${running_jobs[$gpu_id]}" ]]; do
        wait "${running_jobs[$gpu_id]}"
        unset running_jobs[$gpu_id]
    done

    # 启动训练任务，不需要日志
    CUDA_VISIBLE_DEVICES=$gpu_id ${commands[$i]} &

    # 将当前任务的进程 ID 记录到数组中
    running_jobs[$gpu_id]=$!
done

# 等待所有后台任务完成
wait
echo "所有推理任务已完成。"
