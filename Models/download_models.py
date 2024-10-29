from transformers import AutoTokenizer, AutoModelForCausalLM


def load_and_save_model(model_name, save_path):
    """
    加载预训练的模型和tokenizer，并保存到指定路径。

    :param model_name: 预训练模型的名称。
    :param save_path: 保存模型和tokenizer的路径。
    """
    # 加载预训练的tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    # 加载预训练的模型
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # 保存模型到自定义路径
    model.save_pretrained(save_path)
    # 可选：保存tokenizer到相同的路径
    tokenizer.save_pretrained(save_path)


if __name__ == "__main__":
    # 可选，模型仓库名或者本地路径
    MODEL_NAME = 'meta-llama/Llama-3.2-1B'
    SAVE_PATH = f'./{MODEL_NAME}'

    # 调用函数，加载并保存模型
    load_and_save_model(MODEL_NAME, SAVE_PATH)
    print(f"Model and tokenizer saved to {SAVE_PATH}")
