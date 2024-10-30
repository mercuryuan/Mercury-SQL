import torch

print(torch.cuda.is_available())  # 是否可以用gpu False不能，True可以
print(torch.cuda.device_count())  # gpu数量， 0就是没有，1就是检测到了
