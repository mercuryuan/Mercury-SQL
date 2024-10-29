# 欢迎来到Mercury-SQL

## 文件夹概述

简要描述该文件夹的用途。

## 目录结构

列出该文件夹下的主要文件和子文件夹，以及每个文件的简要说明。

## 环境配置

### 安装python3.10

### torch, torchvision, torchaudio安装

以适配cuda为12.1为例

https://pytorch.org/get-started/locally/

```pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121```

### 安装huggingface-cli库

Transformers由三个流行的深度学习库(Jax, PyTorch, TensorFlow)提供支持的预训练先进模型库， 用于
自然语言处理（文本），计算机视觉（图像）、音频和语音处理。

`pip install -U huggingface-hub `

这个有用

### 登录

`huggingface-cli  login`

`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`

`export HF_ENDPOINT=https://hf-mirror.com`

### 下载模型

`huggingface-cli download --resume-download <模型仓库> --local-dir <本地缓存路径>  `
否则默认下载到C:\Users\MaTun\.cache\huggingface里