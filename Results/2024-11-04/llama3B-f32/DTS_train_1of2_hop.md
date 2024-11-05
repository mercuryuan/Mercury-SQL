---
library_name: peft
license: other
base_model: /home/models/Llama-3.2-3B
tags:
- llama-factory
- lora
- generated_from_trainer
model-index:
- name: DTS_train_1of2_hop
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# DTS_train_1of2_hop

This model is a fine-tuned version of [/home/models/Llama-3.2-3B](https://huggingface.co//home/models/Llama-3.2-3B) on the DTS_train_1of2_hop dataset.
It achieves the following results on the evaluation set:
- Loss: 0.0554

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 5e-05
- train_batch_size: 2
- eval_batch_size: 2
- seed: 42
- gradient_accumulation_steps: 8
- total_train_batch_size: 16
- optimizer: Adam with betas=(0.9,0.999) and epsilon=1e-08
- lr_scheduler_type: cosine
- lr_scheduler_warmup_ratio: 0.1
- num_epochs: 5.0

### Training results

| Training Loss | Epoch  | Step | Validation Loss |
|:-------------:|:------:|:----:|:---------------:|
| 0.2431        | 0.2073 | 100  | 0.2315          |
| 0.1539        | 0.4146 | 200  | 0.1412          |
| 0.1073        | 0.6219 | 300  | 0.1234          |
| 0.1004        | 0.8292 | 400  | 0.0994          |
| 0.089         | 1.0365 | 500  | 0.0885          |
| 0.0789        | 1.2438 | 600  | 0.0751          |
| 0.0747        | 1.4512 | 700  | 0.0696          |
| 0.0631        | 1.6585 | 800  | 0.0651          |
| 0.0634        | 1.8658 | 900  | 0.0630          |
| 0.0589        | 2.0731 | 1000 | 0.0611          |
| 0.0567        | 2.2804 | 1100 | 0.0593          |
| 0.0517        | 2.4877 | 1200 | 0.0571          |
| 0.0495        | 2.6950 | 1300 | 0.0572          |
| 0.053         | 2.9023 | 1400 | 0.0568          |
| 0.0481        | 3.1096 | 1500 | 0.0557          |
| 0.0491        | 3.3169 | 1600 | 0.0555          |
| 0.0503        | 3.5242 | 1700 | 0.0556          |
| 0.0476        | 3.7315 | 1800 | 0.0554          |
| 0.0501        | 3.9388 | 1900 | 0.0554          |
| 0.0483        | 4.1462 | 2000 | 0.0554          |
| 0.0487        | 4.3535 | 2100 | 0.0554          |
| 0.0447        | 4.5608 | 2200 | 0.0555          |
| 0.0445        | 4.7681 | 2300 | 0.0554          |
| 0.0475        | 4.9754 | 2400 | 0.0555          |


### Framework versions

- PEFT 0.12.0
- Transformers 4.45.2
- Pytorch 2.5.1+cu121
- Datasets 2.21.0
- Tokenizers 0.20.1