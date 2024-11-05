---
library_name: peft
license: other
base_model: /home/models/Llama-3.2-3B
tags:
- llama-factory
- lora
- generated_from_trainer
model-index:
- name: C3_orig_train_1_hop_lr_55
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# C3_orig_train_1_hop_lr_55

This model is a fine-tuned version of [/home/models/Llama-3.2-3B](https://huggingface.co//home/models/Llama-3.2-3B) on the C3_orig_train_1_hop dataset.
It achieves the following results on the evaluation set:
- Loss: 0.3307

## Model description

More information needed

## Intended uses & limitations

More information needed

## Training and evaluation data

More information needed

## Training procedure

### Training hyperparameters

The following hyperparameters were used during training:
- learning_rate: 5.5e-05
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
| 0.7399        | 0.2540 | 100  | 0.7099          |
| 0.5152        | 0.5079 | 200  | 0.5388          |
| 0.4604        | 0.7619 | 300  | 0.4767          |
| 0.4641        | 1.0159 | 400  | 0.4354          |
| 0.4069        | 1.2698 | 500  | 0.4153          |
| 0.3735        | 1.5238 | 600  | 0.3965          |
| 0.3824        | 1.7778 | 700  | 0.3837          |
| 0.3658        | 2.0317 | 800  | 0.3707          |
| 0.3331        | 2.2857 | 900  | 0.3657          |
| 0.3428        | 2.5397 | 1000 | 0.3535          |
| 0.3306        | 2.7937 | 1100 | 0.3440          |
| 0.303         | 3.0476 | 1200 | 0.3410          |
| 0.2913        | 3.3016 | 1300 | 0.3412          |
| 0.3061        | 3.5556 | 1400 | 0.3370          |
| 0.2739        | 3.8095 | 1500 | 0.3315          |
| 0.2566        | 4.0635 | 1600 | 0.3328          |
| 0.2898        | 4.3175 | 1700 | 0.3315          |
| 0.2847        | 4.5714 | 1800 | 0.3315          |
| 0.2605        | 4.8254 | 1900 | 0.3308          |


### Framework versions

- PEFT 0.12.0
- Transformers 4.45.2
- Pytorch 2.5.1+cu121
- Datasets 2.21.0
- Tokenizers 0.20.1