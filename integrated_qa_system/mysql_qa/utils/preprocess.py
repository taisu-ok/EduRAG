# coding: utf-8
# 导包
import jieba
import os,sys

# 路径
current_dir_path = os.path.dirname(os.path.abspath(__file__))
module_dir_path = os.path.dirname(current_dir_path)
root_path = os.path.dirname(module_dir_path)
sys.path.insert(0, root_path)   # 将根目录添加到系统路径里去

from base import Config, logger


# 定义preprocess_text方法
def preprocess_text(text):
    logger.info("开始预处理文本")
    try:
        return jieba.lcut(text.lower())
    except Exception as e:
        logger.error(f'文本预处理失败:{e}')
        return []

if __name__ == '__main__':
    print(preprocess_text('你好，我是大二电子信息过程专业的大学生'))