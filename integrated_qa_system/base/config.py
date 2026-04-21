# coding: utf-8
# 导包
import configparser
import os

# 解决路径问题，可以在linux和终端上跑
current_file_path = os.path.abspath(__file__)   # 当前的绝对路径
current_dir_path = os.path.dirname(current_file_path) # 当前文件所在目录
project_root = os.path.dirname(current_dir_path)    # 根目录

config_file_path = os.path.join(project_root, "config.ini")

# 配置类
class Config():
    def __init__(self, config_file = config_file_path):
        # 1.创建配置文件解析器
        self.config = configparser.ConfigParser()
        # 2.读取ini配置文件
        self.config.read(config_file, encoding='utf-8')
        # 3.获取相关配置
        # Mysql
        self.MYSQL_HOST = self.config.get('mysql', 'host', fallback= 'localhost')
        self.MYSQL_USER = self.config.get('mysql', 'user', fallback='root')
        self.MYSQL_PASSWORD = self.config.get('mysql', 'password', fallback='123456')
        self.MYSQL_DATABASE = self.config.get('mysql', 'database', fallback='subjects_kg')

        # Redis 配置
        self.REDIS_HOST = self.config.get('redis', 'host', fallback='localhost')
        self.REDIS_PORT = self.config.getint('redis', 'port', fallback=6379)
        self.REDIS_PASSWORD = self.config.get('redis', 'password', fallback='1234')
        self.REDIS_DB = self.config.getint('redis', 'db', fallback=0)

        # Milus 配置
        # Milvus 主机地址
        self.MILVUS_HOST = self.config.get('milvus', 'host', fallback='localhost')
        # Milvus 端口
        self.MILVUS_PORT = self.config.get('milvus', 'port', fallback='19530')
        # Milvus 数据库名
        self.MILVUS_DATABASE_NAME = self.config.get('milvus', 'database_name', fallback='itcast')
        # Milvus 集合名
        self.MILVUS_COLLECTION_NAME = self.config.get('milvus', 'collection_name', fallback='edurag_final')

        # LLM 配置
        # LLM 模型名
        self.LLM_MODEL = self.config.get('llm', 'model', fallback='qwen-plus')
        # DashScope API 密钥
        self.DASHSCOPE_API_KEY = self.config.get('llm', 'dashscope_api_key')
        # DashScope API 地址
        self.DASHSCOPE_BASE_URL = self.config.get('llm', 'dashscope_base_url',
                                                  fallback='https://dashscope.aliyuncs.com/compatible-mode/v1')

        # 检索参数
        # 父块大小
        self.PARENT_CHUNK_SIZE = self.config.getint('retrieval', 'parent_chunk_size', fallback=1200)
        # 子块大小
        self.CHILD_CHUNK_SIZE = self.config.getint('retrieval', 'child_chunk_size', fallback=300)
        # 块重叠大小
        self.CHUNK_OVERLAP = self.config.getint('retrieval', 'chunk_overlap', fallback=50)
        # 检索返回数量
        self.RETRIEVAL_K = self.config.getint('retrieval', 'retrieval_k', fallback=5)
        # 最终候选数量
        self.CANDIDATE_M = self.config.getint('retrieval', 'candidate_m', fallback=2)

        # 应用配置
        self.CUSTOMER_SERVICE_PHONE = self.config.get('app', 'customer_service_phone')
        self.VALID_SOURCES = eval(
            self.config.get('app', 'valid_sources', fallback=["ai", "java", "test", "ops", "bigdata"]))

        # Log配置
        self.LOG_DIR = self.config.get('logger', 'log_dir', fallback='logs')
        self.LOG_FILENAME = self.config.get('logger', 'log_filename', fallback='app.log')


if __name__ == '__main__':
    conf = Config()
    print(conf.LOG_DIR)
    print(conf.LOG_FILENAME)