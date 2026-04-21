# 添加系统路径
import os, sys
mysql_qa_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, mysql_qa_path)

# 导包
from db.mysql_client import MySQLClient
from cache.redis_client import RedisClient
from retrieval.bm25_search import BM25Search