# coding: utf-8
# 导包
import redis
import json
import os, sys

# 路径
current_dir_path = os.path.dirname(os.path.abspath(__file__))
module_dir_path = os.path.dirname(current_dir_path)
root_path = os.path.dirname(module_dir_path)
sys.path.insert(0, root_path)   # 将根目录添加到系统路径里去

from base import Config, logger


# 创建RedisClient类
class RedisClient():
    # init方法
    def __init__(self):
        self.logger = logger    # 初始化日志
        try:
            self.client = redis.StrictRedis(
                host=Config().REDIS_HOST,
                port=Config().REDIS_PORT,
                password=Config().REDIS_PASSWORD,
                db=Config().REDIS_DB,
                decode_responses=True
            )
            self.logger.info("Redis连接成功")   # 记录日志
        except redis.RedisError as e:
            self.logger.error(f"Redis 连接失败:{e}")
            raise

    # set_data方法
    def set_data(self, key, value):
        try:
            self.client.set(key, json.dumps(value, ensure_ascii=False)) # 存储数据
            self.logger.info(f"数据存储到Reids ：{key}")
        except redis.RedisError as e:
            self.logger.error(f'Redis 存储失败:{e}')

    # get_data方法
    def get_data(self, key):
        # 从 Redis 获取数据
        try:
            # 获取数据
            data = self.client.get(key)
            # 返回解析后的 JSON 数据或 None
            return json.loads(data) if data else None
        except redis.RedisError as e:
            # 记录获取失败
            self.logger.error(f"Redis 获取失败: {e}")
            # 返回 None
            return None

    # get_answer方法
    def get_answer(self, query):
        try:
            answer = self.client.get(f'answer:{query}')  # 存储数据
            if answer:
                self.logger.info(f"从 Redis 获取答案:{query}")
                return answer
            return None
        except redis.RedisError as e:
            self.logger.error(f'Redis 查询失败失败:{e}')
            return None



if __name__ == '__main__':
    client = RedisClient()
    client.set_data(1,20)
    # print(client.get_answer("黑马程序员"))
    print(client.get_data(1))