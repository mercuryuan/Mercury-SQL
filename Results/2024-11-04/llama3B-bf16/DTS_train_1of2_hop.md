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
- Loss: 0.0553

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
| 0.243         | 0.2073 | 100  | 0.2315          |
| 0.1537        | 0.4146 | 200  | 0.1432          |
| 0.1072        | 0.6219 | 300  | 0.1232          |
| 0.1006        | 0.8292 | 400  | 0.0996          |
| 0.0885        | 1.0365 | 500  | 0.0893          |
| 0.0783        | 1.2438 | 600  | 0.0751          |
| 0.0749        | 1.4512 | 700  | 0.0694          |
| 0.0624        | 1.6585 | 800  | 0.0646          |
| 0.0628        | 1.8658 | 900  | 0.0630          |
| 0.0581        | 2.0731 | 1000 | 0.0609          |
| 0.0578        | 2.2804 | 1100 | 0.0595          |
| 0.0513        | 2.4877 | 1200 | 0.0573          |
| 0.0494        | 2.6950 | 1300 | 0.0571          |
| 0.0537        | 2.9023 | 1400 | 0.0568          |
| 0.048         | 3.1096 | 1500 | 0.0557          |
| 0.0491        | 3.3169 | 1600 | 0.0554          |
| 0.0505        | 3.5242 | 1700 | 0.0553          |
| 0.0474        | 3.7315 | 1800 | 0.0551          |
| 0.0503        | 3.9388 | 1900 | 0.0552          |
| 0.0484        | 4.1462 | 2000 | 0.0552          |
| 0.0486        | 4.3535 | 2100 | 0.0552          |
| 0.0449        | 4.5608 | 2200 | 0.0553          |
| 0.0446        | 4.7681 | 2300 | 0.0553          |
| 0.0475        | 4.9754 | 2400 | 0.0553          |


### Framework versions

- PEFT 0.12.0
- Transformers 4.45.2
- Pytorch 2.5.1+cu121
- Datasets 2.21.0
- Tokenizers 0.20.1