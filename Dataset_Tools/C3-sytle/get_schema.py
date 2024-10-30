import re
import json
import argparse

from utils.bridge_content_encoder import get_database_matches
from sql_metadata import Parser
from tqdm import tqdm

sql_keywords = ['select', 'from', 'where', 'group', 'order', 'limit', 'intersect', 'union', \
                'except', 'join', 'on', 'as', 'not', 'between', 'in', 'like', 'is', 'exists', 'max', 'min', \
                'count', 'sum', 'avg', 'and', 'or', 'desc', 'asc']


def parse_option():
    """
    解析命令行参数。

    设置并解析运行脚本所需的命令行参数。这些参数包括但不限于模式、数据集路径、数据库路径等，
    用于配置脚本的运行环境和输入输出路径。

    Returns:
        Namespace: 包含解析后的命令行参数的对象。
    """
    # 初始化参数解析器
    parser = argparse.ArgumentParser("")

    # 添加参数解析配置
    parser.add_argument('--mode', type=str, default="train")
    parser.add_argument('--table_path', type=str, default="./data/spider/tables.json")
    parser.add_argument('--input_dataset_path', type=str, default="./data/spider/train_spider.json",
                        help='''
                            options:
                                ./data/spider/train_spider.json
                                ./data/spider/dev.json
                            ''')
    parser.add_argument('--natsql_dataset_path', type=str, default="./NatSQL/NatSQLv1_6/train_spider-natsql.json",
                        help='''
                            options:
                                ./NatSQL/NatSQLv1_6/train_spider-natsql.json
                                ./NatSQL/NatSQLv1_6/dev-natsql.json
                            ''')
    parser.add_argument('--output_dataset_path', type=str, default="./data/pre-processing/preprocessed_dataset.json",
                        help="the filepath of preprocessed dataset.")
    parser.add_argument('--db_path', type=str, default="./data/spider/database",
                        help="the filepath of database.")
    parser.add_argument("--target_type", type=str, default="sql",
                        help="sql or natsql.")
    parser.add_argument("--dataset_name", type=str, default="spider")

    # 解析命令行参数
    opt = parser.parse_args()

    # 返回解析后的参数对象
    return opt


def get_db_contents(question, table_name_original, column_names_original, db_id, db_path):
    """
    从指定数据库表中检索与问题匹配的内容，并按列排序。

    该函数遍历所有列名，调用 `get_database_matches` 函数获取数据库中与问题匹配的内容，对其进行排序，然后将结果添加到匹配内容列表中。

    参数:
    question (str): 要在数据库中匹配的问题。
    table_name_original (str): 表的名称。
    column_names_original (list): 列名列表。
    db_id (str): 数据库的标识符。
    db_path (str): 数据库文件的路径。

    返回值:
    list: 包含每个列匹配内容的列表。
    """
    matched_contents = []
    # 遍历每个列名，提取匹配内容
    for column_name_original in column_names_original:
        matches = get_database_matches(
            question,
            table_name_original,
            column_name_original,
            db_path + "/{}/{}.sqlite".format(db_id, db_id)
        )
        matches = sorted(matches)  # 对匹配内容进行排序
        matched_contents.append(matches)  # 将排序后的匹配内容添加到结果列表中

    return matched_contents


def get_db_schemas(all_db_infos, opt=None):
    db_schemas = {}

    for db in all_db_infos:
        table_names_original = db["table_names_original"]
        table_names = db["table_names"]
        column_names_original = db["column_names_original"]
        column_names = db["column_names"]
        column_types = db["column_types"]

        # 为每个数据库ID初始化一个空字典
        db_schemas[db["db_id"]] = {}

        # 初始化主键和外键列表
        primary_keys, foreign_keys = [], []

        # 记录主键
        # record primary keys
        for pk_column_idx in db["primary_keys"]:
            pk_table_name_original = table_names_original[column_names_original[pk_column_idx][0]]
            pk_column_name_original = column_names_original[pk_column_idx][1]

            primary_keys.append(
                {
                    "table_name_original": pk_table_name_original.lower(),
                    "column_name_original": pk_column_name_original.lower()
                }
            )

        # 将主键列表添加到当前数据库ID的字典中
        db_schemas[db["db_id"]]["pk"] = primary_keys

        # 记录外键
        # record foreign keys
        for source_column_idx, target_column_idx in db["foreign_keys"]:
            fk_source_table_name_original = table_names_original[column_names_original[source_column_idx][0]]
            fk_source_column_name_original = column_names_original[source_column_idx][1]

            fk_target_table_name_original = table_names_original[column_names_original[target_column_idx][0]]
            fk_target_column_name_original = column_names_original[target_column_idx][1]

            foreign_keys.append(
                {
                    "source_table_name_original": fk_source_table_name_original.lower(),
                    "source_column_name_original": fk_source_column_name_original.lower(),
                    "target_table_name_original": fk_target_table_name_original.lower(),
                    "target_column_name_original": fk_target_column_name_original.lower(),
                }
            )
        # 将外键列表添加到当前数据库ID的字典中
        db_schemas[db["db_id"]]["fk"] = foreign_keys

        # 初始化schema_items列表
        db_schemas[db["db_id"]]["schema_items"] = []

        # 遍历每个原始表名
        for idx, table_name_original in enumerate(table_names_original):
            column_names_original_list = []
            column_names_list = []
            column_types_list = []

            # 遍历每个列名
            for column_idx, (table_idx, column_name_original) in enumerate(column_names_original):
                if idx == table_idx:
                    # 将当前表的列名添加到相应列表中
                    column_names_original_list.append(column_name_original.lower())
                    column_names_list.append(column_names[column_idx][1].lower())
                    column_types_list.append(column_types[column_idx])

            # 将当前表的schema信息添加到当前数据库ID的字典中
            db_schemas[db["db_id"]]["schema_items"].append({
                "table_name_original": table_name_original.lower(),
                "table_name": table_names[idx].lower(),
                "column_names": column_names_list,
                "column_names_original": column_names_original_list,
                "column_types": column_types_list
            })

    return db_schemas


def normalization(sql):
    def white_space_fix(s):
        parsed_s = Parser(s)
        # 将解析后的token值用空格连接成字符串
        s = " ".join([token.value for token in parsed_s.tokens])

        return s

    # 将非单引号内的文本转换为小写
    def lower(s):
        in_quotation = False
        out_s = ""
        for char in s:
            if in_quotation:
                out_s += char
            else:
                # 将字符转换为小写并添加到输出字符串中
                out_s += char.lower()

            if char == "'":
                if in_quotation:
                    in_quotation = False
                else:
                    in_quotation = True

        return out_s

    # 移除字符串末尾的分号
    def remove_semicolon(s):
        if s.endswith(";"):
            s = s[:-1]
        return s

    # 将双引号替换为单引号
    def double2single(s):
        return s.replace("\"", "'")

    # 在ORDER BY子句中未指定排序方式时，默认添加ASC排序
    def add_asc(s):
        pattern = re.compile(
            r'order by (?:\w+ \( \S+ \)|\w+\.\w+|\w+)(?: (?:\+|\-|\<|\<\=|\>|\>\=) (?:\w+ \( \S+ \)|\w+\.\w+|\w+))*')
        if "order by" in s and "asc" not in s and "desc" not in s:
            for p_str in pattern.findall(s):
                # 将找到的ORDER BY子句后添加ASC排序
                s = s.replace(p_str, p_str + " asc")

        return s

    # 移除表别名，并用实际的表名替换别名
    def remove_table_alias(s):
        tables_aliases = Parser(s).tables_aliases
        new_tables_aliases = {}
        for i in range(1, 11):
            if "t{}".format(i) in tables_aliases.keys():
                new_tables_aliases["t{}".format(i)] = tables_aliases["t{}".format(i)]

        tables_aliases = new_tables_aliases
        for k, v in tables_aliases.items():
            # 移除AS关键字和别名
            s = s.replace("as " + k + " ", "")
            # 用实际的表名替换别名
            s = s.replace(k, v)

        return s

    # 定义处理函数，按照定义的顺序依次执行各个处理函数
    processing_func = lambda x: remove_table_alias(add_asc(lower(white_space_fix(double2single(remove_semicolon(x))))))

    return processing_func(sql)


# extract the skeleton of sql and natsql
def extract_skeleton(sql, db_schema):
    # 初始化三个列表，用于存储原始表名、原始表名加点列名和原始列名
    table_names_original, table_dot_column_names_original, column_names_original = [], [], []
    for table in db_schema["schema_items"]:
        table_name_original = table["table_name_original"]
        # 将原始表名添加到table_names_original列表中
        table_names_original.append(table_name_original)

        # 遍历表中的所有列名，包括'*'作为通配符
        for column_name_original in ["*"] + table["column_names_original"]:
            # 将原始表名加点列名添加到table_dot_column_names_original列表中
            table_dot_column_names_original.append(table_name_original + "." + column_name_original)
            # 将原始列名添加到column_names_original列表中
            column_names_original.append(column_name_original)

    # 解析SQL语句
    parsed_sql = Parser(sql)
    new_sql_tokens = []
    # 遍历解析后的SQL语句中的每个token
    for token in parsed_sql.tokens:
        # 掩码表名
        if token.value in table_names_original:
            new_sql_tokens.append("_")
        # 掩码列名
        elif token.value in column_names_original \
                or token.value in table_dot_column_names_original:
            new_sql_tokens.append("_")
        # 掩码字符串值
        elif token.value.startswith("'") and token.value.endswith("'"):
            new_sql_tokens.append("_")
        # 掩码正整数
        elif token.value.isdigit():
            new_sql_tokens.append("_")
        # 掩码负整数
        elif isNegativeInt(token.value):
            new_sql_tokens.append("_")
        # 掩码浮点数
        elif isFloat(token.value):
            new_sql_tokens.append("_")
        else:
            # 否则，将token值去除首尾空白字符后添加到new_sql_tokens列表中
            new_sql_tokens.append(token.value.strip())

    # 将new_sql_tokens列表中的元素用空格连接成字符串，得到SQL骨架
    sql_skeleton = " ".join(new_sql_tokens)

    # 移除JOIN ON关键字
    sql_skeleton = sql_skeleton.replace("on _ = _ and _ = _", "on _ = _")
    sql_skeleton = sql_skeleton.replace("on _ = _ or _ = _", "on _ = _")
    sql_skeleton = sql_skeleton.replace(" on _ = _", "")
    pattern3 = re.compile("_ (?:join _ ?)+")
    sql_skeleton = re.sub(pattern3, "_ ", sql_skeleton)

    # 将连续的"_ , _"替换为"_"
    # "_ , _ , ..., _" -> "_"
    while ("_ , _" in sql_skeleton):
        sql_skeleton = sql_skeleton.replace("_ , _", "_")

    # 移除WHERE关键字中的子句
    ops = ["=", "!=", ">", ">=", "<", "<="]
    for op in ops:
        if "_ {} _".format(op) in sql_skeleton:
            sql_skeleton = sql_skeleton.replace("_ {} _".format(op), "_")
    # 移除WHERE子句中的逻辑运算符
    while ("where _ and _" in sql_skeleton or "where _ or _" in sql_skeleton):
        if "where _ and _" in sql_skeleton:
            sql_skeleton = sql_skeleton.replace("where _ and _", "where _")
        if "where _ or _" in sql_skeleton:
            sql_skeleton = sql_skeleton.replace("where _ or _", "where _")

    # 移除骨架中的多余空格
    while "  " in sql_skeleton:
        sql_skeleton = sql_skeleton.replace("  ", " ")

    return sql_skeleton


def isNegativeInt(string):
    # 如果字符串以"-"开头且"-"之后的字符都是数字
    if string.startswith("-") and string[1:].isdigit():
        return True
    else:
        # 如果不满足条件，返回False
        return False


def isFloat(string):
    # 如果字符串以"-"开头，则去除"-"
    if string.startswith("-"):
        string = string[1:]

    # 将字符串以"."为分隔符进行分割
    s = string.split(".")
    # 如果分割后的列表长度大于2，则说明存在多于一个"."，不符合浮点数规则
    if len(s) > 2:
        return False
    else:
        # 遍历分割后的每个子字符串
        for s_i in s:
            # 如果子字符串不是全数字，则返回False
            if not s_i.isdigit():
                return False
        # 如果所有子字符串都是全数字，则返回True
        return True


def main(opt):
    # 加载数据集
    dataset = json.load(open(opt.input_dataset_path))
    # 加载数据库信息
    all_db_infos = json.load(open(opt.table_path))

    # 确保操作模式在允许的范围内
    assert opt.mode in ["train", "eval", "test"]

    # 如果操作模式为训练或评估，并且目标类型为NATSQL，则加载NATSQL数据集
    if opt.mode in ["train", "eval"] and opt.target_type == "natsql":
        # only train_spider.json and dev.json have corresponding natsql dataset
        # 只有train_spider.json和dev.json有对应的NATSQL数据集
        natsql_dataset = json.load(open(opt.natsql_dataset_path))
    else:
        # empty natsql dataset
        # 空NATSQL数据集
        natsql_dataset = [None for _ in range(len(dataset))]

    # 获取数据库架构
    db_schemas = get_db_schemas(all_db_infos, opt)

    # 初始化预处理后的数据集
    preprocessed_dataset = []

    # 遍历数据集和NATSQL数据集
    for natsql_data, data in tqdm(zip(natsql_dataset, dataset)):
        # 如果查询匹配特定字符串，则进行替换
        if data[
            'query'] == 'SELECT T1.company_name FROM Third_Party_Companies AS T1 JOIN Maintenance_Contracts AS T2 ON T1.company_id  =  T2.maintenance_contract_company_id JOIN Ref_Company_Types AS T3 ON T1.company_type_code  =  T3.company_type_code ORDER BY T2.contract_end_date DESC LIMIT 1':
            data[
                'query'] = '老子被替换啦？SELECT T1.company_type FROM Third_Party_Companies AS T1 JOIN Maintenance_Contracts AS T2 ON T1.company_id  =  T2.maintenance_contract_company_id ORDER BY T2.contract_end_date DESC LIMIT 1'
            data['query_toks'] = ['SELECT', 'T1.company_type', 'FROM', 'Third_Party_Companies', 'AS', 'T1', 'JOIN',
                                  'Maintenance_Contracts', 'AS', 'T2', 'ON', 'T1.company_id', '=',
                                  'T2.maintenance_contract_company_id', 'ORDER', 'BY', 'T2.contract_end_date',
                                  'DESC',
                                  'LIMIT', '1']
            data['query_toks_no_value'] = ['select', 't1', '.', 'company_type', 'from', 'third_party_companies',
                                           'as',
                                           't1', 'join', 'maintenance_contracts', 'as', 't2', 'on', 't1', '.',
                                           'company_id', '=', 't2', '.', 'maintenance_contract_company_id', 'order',
                                           'by', 't2', '.', 'contract_end_date', 'desc', 'limit', 'value']
            data['question'] = 'What is the type of the company who concluded its contracts most recently?'
            data['question_toks'] = ['What', 'is', 'the', 'type', 'of', 'the', 'company', 'who', 'concluded', 'its',
                                     'contracts', 'most', 'recently', '?']
        # 如果查询以特定字符串开头，则进行替换
        if data['query'].startswith(
                'SELECT T1.fname FROM student AS T1 JOIN lives_in AS T2 ON T1.stuid  =  T2.stuid WHERE T2.dormid IN'):
            data['query'] = data['query'].replace('IN (SELECT T2.dormid)', 'IN (SELECT T3.dormid)我也被替换了')
            index = data['query_toks'].index('(') + 2
            assert data['query_toks'][index] == 'T2.dormid'
            data['query_toks'][index] = 'T3.dormid'
            index = data['query_toks_no_value'].index('(') + 2
            assert data['query_toks_no_value'][index] == 't2'
            data['query_toks_no_value'][index] = 't3'

        # 清理问题字符串
        question = data["question"].replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", "'").replace(
            "\u201d", "'").strip()
        # 获取数据库ID
        db_id = data["db_id"]

        # 如果是测试模式，则初始化SQL和NATSQL相关变量为空字符串
        if opt.mode == "test":
            sql, norm_sql, sql_skeleton = "", "", ""
            sql_tokens = []

            natsql, norm_natsql, natsql_skeleton = "", "", ""
            natsql_used_columns, natsql_tokens = [], []
        else:

            # 获取SQL查询
            sql = data["query"].strip()
            # 规范化SQL查询
            norm_sql = normalization(sql).strip()
            # 提取SQL骨架
            sql_skeleton = extract_skeleton(norm_sql, db_schemas[db_id]).strip()
            # 分割规范化SQL查询为单词列表
            sql_tokens = norm_sql.split()

            # 如果存在NATSQL数据，则处理NATSQL查询
            if natsql_data is not None:
                natsql = natsql_data["NatSQL"].strip()
                norm_natsql = normalization(natsql).strip()
                natsql_skeleton = extract_skeleton(norm_natsql, db_schemas[db_id]).strip()
                # 提取NATSQL查询中使用的列
                natsql_used_columns = [token for token in norm_natsql.split() if "." in token and token != "@.@"]
                natsql_tokens = []
                for token in norm_natsql.split():
                    # split table_name_original.column_name_original
                    if "." in token:
                        natsql_tokens.extend(token.split("."))
                    else:
                        natsql_tokens.append(token)
            else:
                natsql, norm_natsql, natsql_skeleton = "", "", ""
                natsql_used_columns, natsql_tokens = [], []

        # 初始化预处理后的数据字典
        preprocessed_data = {}
        preprocessed_data["question"] = question
        preprocessed_data["db_id"] = db_id

        # 设置SQL相关字段
        preprocessed_data["sql"] = sql
        preprocessed_data["norm_sql"] = norm_sql
        preprocessed_data["sql_skeleton"] = sql_skeleton

        # 设置NATSQL相关字段
        preprocessed_data["natsql"] = natsql
        preprocessed_data["norm_natsql"] = norm_natsql
        preprocessed_data["natsql_skeleton"] = natsql_skeleton

        # 初始化数据库架构列表
        preprocessed_data["db_schema"] = []
        # 设置主键和外键
        preprocessed_data["pk"] = db_schemas[db_id]["pk"]
        preprocessed_data["fk"] = db_schemas[db_id]["fk"]
        # 初始化表和列标签列表
        preprocessed_data["table_labels"] = []
        preprocessed_data["column_labels"] = []

        # 添加数据库信息（包括表名、列名等）
        # add database information (including table name, column name, ..., table_labels, and column labels)
        for table in db_schemas[db_id]["schema_items"]:
            # 获取数据库内容
            db_contents = get_db_contents(
                question,
                table["table_name_original"],
                table["column_names_original"],
                db_id,
                opt.db_path
            )

            # 将数据库信息添加到预处理后的数据字典中
            preprocessed_data["db_schema"].append({
                "table_name_original": table["table_name_original"],
                "table_name": table["table_name"],
                "column_names": table["column_names"],
                "column_names_original": table["column_names_original"],
                "column_types": table["column_types"],
                "db_contents": db_contents
            })

            '''
                提取表和列的分类标签
                table_labels 和 column_labels 分别代表了表和列的分类标签。

                table_labels：这是一个列表，用于存储每个表的标签。如果表在SQL查询（或NATSQL查询）中被使用，则对应的标签为1；如果表未被使用，则标签为0。

                column_labels：这是一个列表的列表（二维列表），用于存储每个表中每列的标签。如果某列在SQL查询（或NATSQL查询）中被使用，则对应的标签为1；如果列未被使用，则标签为0。

                这种标签机制通常用于机器学习或数据预处理阶段，以便后续模型能够识别出哪些表和列在特定的查询中被使用
            '''
            # 判断目标类型是否为sql
            if opt.target_type == "sql":
                # 判断表名是否在sql_tokens中，即是否为已使用的表
                if table["table_name_original"] in sql_tokens:  # for used tables
                    # 将表标签设为1，表示该表被使用
                    preprocessed_data["table_labels"].append(1)
                    # 初始化列标签列表
                    column_labels = []
                    # 遍历表的原始列名
                    for column_name_original in table["column_names_original"]:
                        # 判断列名是否在sql_tokens中或表名加列名的组合在sql_tokens中，即是否为已使用的列
                        if column_name_original in sql_tokens or \
                                table[
                                    "table_name_original"] + "." + column_name_original in sql_tokens:  # for used columns
                            # 将列标签设为1，表示该列被使用
                            column_labels.append(1)
                        else:
                            # 将列标签设为0，表示该列未被使用
                            column_labels.append(0)
                    # 将列标签列表添加到preprocessed_data中
                    preprocessed_data["column_labels"].append(column_labels)
                else:  # for unused tables and their columns
                    # 将表标签设为0，表示该表未被使用
                    preprocessed_data["table_labels"].append(0)
                    # 初始化一个与表列数相同的全0列表，表示所有列都未被使用
                    preprocessed_data["column_labels"].append([0 for _ in range(len(table["column_names_original"]))])
            # 判断目标类型是否为natsql
            elif opt.target_type == "natsql":
                # 判断表名是否在natsql_tokens中，即是否为已使用的表
                if table["table_name_original"] in natsql_tokens:  # for used tables
                    # 将表标签设为1，表示该表被使用
                    preprocessed_data["table_labels"].append(1)
                    # 初始化列标签列表
                    column_labels = []
                    # 遍历表的原始列名
                    for column_name_original in table["column_names_original"]:
                        # 判断表名加列名的组合是否在natsql_used_columns中，即是否为已使用的列
                        if table[
                            "table_name_original"] + "." + column_name_original in natsql_used_columns:  # for used columns
                            # 将列标签设为1，表示该列被使用
                            column_labels.append(1)
                        else:
                            # 将列标签设为0，表示该列未被使用
                            column_labels.append(0)
                    # 将列标签列表添加到preprocessed_data中
                    preprocessed_data["column_labels"].append(column_labels)
                else:
                    # 将表标签设为0，表示该表未被使用
                    preprocessed_data["table_labels"].append(0)
                    # 初始化一个与表列数相同的全0列表，表示所有列都未被使用
                    preprocessed_data["column_labels"].append([0 for _ in range(len(table["column_names_original"]))])
            else:
                # 如果目标类型既不是sql也不是natsql，则抛出异常
                raise ValueError("target_type should be ``sql'' or ``natsql''")

        # 将预处理后的数据添加到预处理后的数据集中
        preprocessed_dataset.append(preprocessed_data)

    # 将预处理后的数据集保存到文件中
    with open(opt.output_dataset_path, "w") as f:
        preprocessed_dataset_str = json.dumps(preprocessed_dataset, indent=2)
        f.write(preprocessed_dataset_str)


if __name__ == "__main__":
    opt = parse_option()
    main(opt)
