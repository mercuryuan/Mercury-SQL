---
library_name: peft
license: other
base_model: /home/models/Llama-3.2-3B
tags:
- llama-factory
- lora
- generated_from_trainer
model-index:
- name: C3_train_1_hop
  results: []
---

<!-- This model card has been generated automatically according to the information the Trainer had access to. You
should probably proofread and complete it, then remove this comment. -->

# C3_train_1_hop

This model is a fine-tuned version of [/home/models/Llama-3.2-3B](https://huggingface.co//home/models/Llama-3.2-3B) on the C3_train_1_hop dataset.
It achieves the following results on the evaluation set:
- Loss: 0.3311

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
| 0.7627        | 0.2540 | 100  | 0.7134          |
| 0.5149        | 0.5079 | 200  | 0.5423          |
| 0.4726        | 0.7619 | 300  | 0.4803          |
| 0.4597        | 1.0159 | 400  | 0.4338          |
| 0.4033        | 1.2698 | 500  | 0.4110          |
| 0.3667        | 1.5238 | 600  | 0.3963          |
| 0.3756        | 1.7778 | 700  | 0.3809          |
| 0.3589        | 2.0317 | 800  | 0.3743          |
| 0.3266        | 2.2857 | 900  | 0.3699          |
| 0.345         | 2.5397 | 1000 | 0.3557          |
| 0.3326        | 2.7937 | 1100 | 0.3466          |
| 0.3055        | 3.0476 | 1200 | 0.3415          |
| 0.2872        | 3.3016 | 1300 | 0.3418          |
| 0.3037        | 3.5556 | 1400 | 0.3360          |
| 0.2721        | 3.8095 | 1500 | 0.3308          |
| 0.258         | 4.0635 | 1600 | 0.3301          |
| 0.2876        | 4.3175 | 1700 | 0.3315          |
| 0.2849        | 4.5714 | 1800 | 0.3315          |
| 0.2617        | 4.8254 | 1900 | 0.3312          |


### Framework versions

- PEFT 0.12.0
- Transformers 4.45.2
- Pytorch 2.5.1+cu121
- Datasets 2.21.0
- Tokenizers 0.20.1