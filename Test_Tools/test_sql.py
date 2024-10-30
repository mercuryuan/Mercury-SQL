"""
本模块用于测试SQLite数据库的连接和查询功能。
"""
import sys
import os
import pickle as pkl
from typing import Tuple, Any
import sqlite3
import re


def replace_cur_year(query: str) -> str:
    """
    替换SQL查询中的当前年份。

    Args:
        query (str): 要执行的SQL查询语句。

    Returns:
        str: 替换当前年份后的SQL查询语句。

    """
    return re.sub(
        "YEAR\s*\(\s*CURDATE\s*\(\s*\)\s*\)\s*", "2020", query, flags=re.IGNORECASE
    )


def get_cursor_from_path(sqlite_path: str) -> sqlite3.Cursor:
    """
    从指定的SQLite数据库路径获取游标对象。

    Args:
        sqlite_path (str): SQLite数据库文件的路径。

    Returns:
        sqlite3.Cursor: 返回SQLite数据库的连接游标对象。

    Raises:
        Exception: 如果无法连接到SQLite数据库，将抛出异常。

    """
    try:
        if not os.path.exists(sqlite_path):
            print('Openning a new connection %s' % sqlite_path)
        connection = sqlite3.connect(sqlite_path)
    except Exception as e:
        print(sqlite_path)
        raise e
    connection.text_factory = lambda b: b.decode(errors='ignore')
    cursor = connection.cursor()
    return cursor


def exec_on_db(sqlite_path: str, query: str) -> Tuple[str, Any]:
    """
    执行数据库查询，并返回查询结果或异常信息。

    Args:
        sqlite_path (str): SQLite数据库文件的路径。
        query (str): 要执行的SQL查询语句。

    Returns:
        Tuple[str, Any]: 一个元组，包含执行结果。第一个元素为字符串类型，表示执行状态，可以是'result'或'exception'；第二个元素为Any类型，如果是'result'，则为查询结果列表，如果是'exception'，则为异常信息。

    """
    query = replace_cur_year(query)
    cursor = get_cursor_from_path(sqlite_path)
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return 'result', result
    except Exception as e:
        cursor.close()
        return 'exception', e


# 示例用法
if __name__ == "__main__":
    sqlite_path = "../spider/database/world_1/world_1.sqlite"  # 替换为你的数据库路径
    query = "SELECT sum(SurfaceArea) FROM country WHERE Region = 'Caribbean'"  # 替换为你的SQL查询语句
    result = exec_on_db(sqlite_path, query)
    if result[0] == 'result':
        # 处理查询结果
        print(result[1])
    else:
        # 处理异常信息
        print(result[1])
