# coding: utf-8
# 导包
import logging  # 日志库
import os   # 导入路径操作库
from config import Config   # 导入Config类

# 路径配置，可以在linux，终端运行代码
current_file_path = os.path.abspath(__file__)   # 当前文件的绝对路径
current_dir_path = os.path.dirname(current_file_path)   # 当前目录
project_root = os.path.dirname(current_dir_path)    # 当前根目录，绝对路径


# 获取日志路径
log_dir_path = os.path.join(project_root, Config().LOG_DIR)
log_file_path = os.path.join(log_dir_path, Config().LOG_FILENAME)


# 定义setup_logging方法，创建日志器
def setup_logging(log_file=log_file_path):
    # 创建日志目录
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    # 获取日志器
    logger = logging.getLogger("EduRAG")
    # 设置日志级别
    logger.setLevel(logging.DEBUG)
    # 避免重复添加处理器
    if not logger.handlers:
        # 创建文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        # 设置文件处理器的级别
        file_handler.setLevel(logging.DEBUG)
        # 创建控制台处理器
        console_handle = logging.StreamHandler()
        # 设置控制台处理器的级别
        console_handle.setLevel(logging.INFO)
        # 设置日志格式
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # 为文件处理器设置格式
        file_handler.setFormatter(formatter)
        # 为控制台处理器设置格式
        console_handle.setFormatter(formatter)
        # 添加文件处理器
        logger.addHandler(file_handler)
        # 添加控制台处理器
        logger.addHandler(console_handle)

    # 返回日志器
    return logger

logger = setup_logging()

if __name__ == '__main__':
    logger.info('测试一下')
