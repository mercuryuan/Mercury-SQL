---
library_name: peft
license: other
base_model: /home/models/Llama-3.2-3B
tags:
- llama-factory
- lora
- generated_from_trainer
model-index:
- name: C3_orig_train_1_hop_lr_5
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# C3_orig_train_1_hop_lr_5

This model is a fine-tuned version of [/home/models/Llama-3.2-3B](https://huggingface.co//home/models/Llama-3.2-3B) on the C3_orig_train_1_hop dataset.
It achieves the following results on the evaluation set:
- Loss: 0.3338

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
| 0.7594        | 0.2540 | 100  | 0.7326          |
| 0.5206        | 0.5079 | 200  | 0.5458          |
| 0.4664        | 0.7619 | 300  | 0.4832          |
| 0.4685        | 1.0159 | 400  | 0.4392          |
| 0.4096        | 1.2698 | 500  | 0.4165          |
| 0.3768        | 1.5238 | 600  | 0.4010          |
| 0.3855        | 1.7778 | 700  | 0.3877          |
| 0.3692        | 2.0317 | 800  | 0.3735          |
| 0.3378        | 2.2857 | 900  | 0.3683          |
| 0.3463        | 2.5397 | 1000 | 0.3594          |
| 0.3369        | 2.7937 | 1100 | 0.3489          |
| 0.3082        | 3.0476 | 1200 | 0.3456          |
| 0.2931        | 3.3016 | 1300 | 0.3454          |
| 0.3098        | 3.5556 | 1400 | 0.3401          |
| 0.2787        | 3.8095 | 1500 | 0.3335          |
| 0.2602        | 4.0635 | 1600 | 0.3367          |
| 0.2954        | 4.3175 | 1700 | 0.3351          |
| 0.2897        | 4.5714 | 1800 | 0.3344          |
| 0.2649        | 4.8254 | 1900 | 0.3337          |


### Framework versions

- PEFT 0.12.0
- Transformers 4.45.2
- Pytorch 2.5.1+cu121
- Datasets 2.21.0
- Tokenizers 0.20.1