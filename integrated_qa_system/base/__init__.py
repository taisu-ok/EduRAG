# 导包
import os
import sys

# 获取当前所在目录绝对路径
current_dir_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir_path)

# 将当前目录路径 和 根目录添加到系统路径里面
if current_dir_path not in sys.path:
    sys.path.insert(0, current_dir_path)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from config import Config
from logger import logger




