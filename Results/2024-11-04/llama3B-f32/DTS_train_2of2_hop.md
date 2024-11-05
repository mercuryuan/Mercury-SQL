---
library_name: peft
license: other
base_model: /home/models/Llama-3.2-3B
tags:
- llama-factory
- lora
- generated_from_trainer
model-index:
- name: DTS_train_2of2_hop
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# DTS_train_2of2_hop

This model is a fine-tuned version of [/home/models/Llama-3.2-3B](https://huggingface.co//home/models/Llama-3.2-3B) on the DTS_train_2of2_hop dataset.
It achieves the following results on the evaluation set:
- Loss: 0.2820

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
| 0.609         | 0.2073 | 100  | 0.5884          |
| 0.4357        | 0.4146 | 200  | 0.4019          |
| 0.3463        | 0.6219 | 300  | 0.3604          |
| 0.3311        | 0.8292 | 400  | 0.3352          |
| 0.2961        | 1.0365 | 500  | 0.3283          |
| 0.2827        | 1.2438 | 600  | 0.3198          |
| 0.322         | 1.4512 | 700  | 0.3124          |
| 0.2947        | 1.6585 | 800  | 0.3047          |
| 0.3041        | 1.8658 | 900  | 0.3025          |
| 0.2861        | 2.0731 | 1000 | 0.2983          |
| 0.289         | 2.2804 | 1100 | 0.2923          |
| 0.2609        | 2.4877 | 1200 | 0.2877          |
| 0.273         | 2.6950 | 1300 | 0.2871          |
| 0.2682        | 2.9023 | 1400 | 0.2840          |
| 0.2411        | 3.1096 | 1500 | 0.2886          |
| 0.254         | 3.3169 | 1600 | 0.2836          |
| 0.2791        | 3.5242 | 1700 | 0.2827          |
| 0.2361        | 3.7315 | 1800 | 0.2805          |
| 0.243         | 3.9388 | 1900 | 0.2799          |
| 0.2251        | 4.1462 | 2000 | 0.2822          |
| 0.2761        | 4.3535 | 2100 | 0.2819          |
| 0.215         | 4.5608 | 2200 | 0.2824          |
| 0.2241        | 4.7681 | 2300 | 0.2822          |
| 0.2399        | 4.9754 | 2400 | 0.2822          |


### Framework versions

- PEFT 0.12.0
- Transformers 4.45.2
- Pytorch 2.5.1+cu121
- Datasets 2.21.0
- Tokenizers 0.20.1