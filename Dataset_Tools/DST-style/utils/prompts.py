def sql_generation_prompt_token_counter(question, database_schema, query, tokenizer):
    user_message = f"""Given the following SQL tables, your job is to generate the Sqlite SQL query given the user's question.
    Put your answer inside the ```sql and ``` tags.
    {database_schema}
    ###
    Question: {question}
    """
    assitant_message = f"""
    ```sql
    {query} ;
    ```
    <|EOT|>
    """
    messages = [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": assitant_message},
    ]
    return len(tokenizer.apply_chat_template(messages, tokenize=True))


def schema_linking_prompt_token_counter(
    question, database_schema, correct_tables, correct_columns, tokenizer
):
    """
    统计在schema linking提示中使用的token数量。

    Args:
        question (str): 用户提出的问题。
        database_schema (str): 数据库的模式，包括表的结构信息。
        correct_tables (list): 用户问题中涉及的正确表名列表。
        correct_columns (list): 用户问题中涉及的正确列名列表。
        tokenizer (Tokenizer): 用于文本分词的工具类。

    Returns:
        int: 在schema linking提示中使用的token数量。

    """
    user_message = f"""Given the following SQL tables, your job is to determine the column names and table that the question is referring to.
{database_schema}
###
Question: {question}
"""
    assitant_message = f"""
Columns: {correct_columns}
Tables: {correct_tables}
 ;
"""
    messages = [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": assitant_message},
    ]
    # 调用tokenizer的apply_chat_template方法，传入messages列表和tokenize=True参数
    # 该方法会对messages中的文本进行分词处理，并返回分词后的token列表
    # 返回分词后token列表的长度
    return len(tokenizer.apply_chat_template(messages, tokenize=True))

