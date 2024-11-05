#!/bin/bash
MODEL_NAME="llama3B"
# 获取当前日期，并格式化为 YYYY-MM-DD
current_date=$(date +%F)

# 检查文件夹是否已经存在
if [ ! -d "Results/$current_date" ]; then
    # 创建以当前日期命名的文件夹
    mkdir "Results/$current_date"
    echo "文件夹 'Results/$current_date' 已创建。"
else
    echo "文件夹 'Results/$current_date' 已存在。"
fi
# 创建llama3B文件夹
if [ ! -d "Results/$current_date/$MODEL_NAME" ]; then
    # 创建以当前日期命名的文件夹
    mkdir "Results/$current_date/$MODEL_NAME"
    echo "文件夹 'Results/$current_date/$MODEL_NAME' 已创建。"
else
    echo "文件夹 'Results/$current_date/$MODEL_NAME' 已存在。"
fi