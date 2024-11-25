import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 常用路径配置
BIRD_DATA_PATH = os.path.join(BASE_DIR, "Datasets/BIRD_dev/dev_databases")
BIRD_TRAIN_PATH = os.path.join(BASE_DIR,
                               "D:/Users/MaTun/Downloads/data/data/sft_data_collections/bird/train/train_databases")
SPIDER_DATA_PATH = os.path.join(BASE_DIR, "Datasets/spider/database")
TRAIN_OTHERS_PATH = os.path.join(BASE_DIR, "Datasets/spider/train_others.json")
TRAIN_SPIDER_PATH = os.path.join(BASE_DIR, "Datasets/spider/train_spider.json")
DEV_PATH = os.path.join(BASE_DIR, "Datasets/spider/dev.json")
DATA_OUTPUT_DIR = os.path.join(BASE_DIR, "Data/DTS-data")
DATASET_OUTPUT_DIR = os.path.join(BASE_DIR, "Datasets/DTS-data")

if __name__ == '__main__':
    print(BASE_DIR)
