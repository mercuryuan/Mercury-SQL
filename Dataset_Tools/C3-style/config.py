import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 常用路径配置
SPIDER_DATA_PATH = os.path.join(BASE_DIR, "Datasets/spider/database")
TRAIN_OTHERS_PATH = os.path.join(BASE_DIR, "Datasets/spider/train_others.json")
TRAIN_SPIDER_PATH = os.path.join(BASE_DIR, "Datasets/spider/train_spider.json")
TABLE_PATH = os.path.join(BASE_DIR, "Datasets/spider/table.json")
DEV_PATH = os.path.join(BASE_DIR, "Datasets/spider/dev.json")
DATA_OUTPUT_DIR = os.path.join(BASE_DIR, "Data/")
DATASET_OUTPUT_DIR = os.path.join(BASE_DIR, "Training_Dataset/")

if __name__ == '__main__':
    # 设置环境变量
    os.environ['BASE_DIR'] = BASE_DIR
    os.environ['SPIDER_DATA_PATH'] = SPIDER_DATA_PATH
    os.environ['TRAIN_OTHERS_PATH'] = TRAIN_OTHERS_PATH
    os.environ['TRAIN_SPIDER_PATH'] = TRAIN_SPIDER_PATH
    os.environ['TABLE_PATH'] = TABLE_PATH
    os.environ['DEV_PATH'] = DEV_PATH
    os.environ['DATA_OUTPUT_DIR'] = DATA_OUTPUT_DIR
    os.environ['DATASET_OUTPUT_DIR'] = DATASET_OUTPUT_DIR

    # 打印环境变量（可选，用于验证）
    print("BASE_DIR:", os.environ['BASE_DIR'])
    print("SPIDER_DATA_PATH:", os.environ['SPIDER_DATA_PATH'])
    print("TRAIN_OTHERS_PATH:", os.environ['TRAIN_OTHERS_PATH'])
    print("TRAIN_SPIDER_PATH:", os.environ['TRAIN_SPIDER_PATH'])
    print("TABLE_PATH:", os.environ['TABLE_PATH'])
    print("DEV_PATH:", os.environ['DEV_PATH'])
    print("DATA_OUTPUT_DIR:", os.environ['DATA_OUTPUT_DIR'])
    print("DATASET_OUTPUT_DIR:", os.environ['DATASET_OUTPUT_DIR'])
