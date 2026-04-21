# coding: utf-8
# 导包
import logging

# 创建日志记录器
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 创建文件处理器
file_handler = logging.FileHandler('app.log', mode= "a")
file_handler.setLevel(logging.DEBUG)

# 定义日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 为处理器设置格式
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 将处理器添加到记录器中
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 记录日志
logger.debug("This is a debug message")
logger.info("This is an info message")
logger.error("This is an error message")