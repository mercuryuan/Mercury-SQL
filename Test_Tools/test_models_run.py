from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# 确保PyTorch可以访问GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

model_name = "meta-llama/Llama-3.1-8B"  # 跑不了，显存不足
# llama3B = "E:\Models\Llama-3.2-3B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 将模型移动到GPU
model.to(device)

# 输入准备：准备输入文本并进行tokenization。
input_text = "Please tell me the way to station."
inputs = tokenizer(input_text, return_tensors="pt")

# 将输入数据移动到GPU
inputs = inputs.to(device)

# 模型推理：将tokenized的输入传递给模型，并获取输出。
outputs = model.generate(**inputs, max_length=124)

# 解码输出，并将其移回CPU（如果需要）
decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(decoded_output)
