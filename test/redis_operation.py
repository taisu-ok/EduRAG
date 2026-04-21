import redis
import json
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

class RedisClient:
    def __init__(self):
        self.logger = logger
        try:
            self.client = redis.StrictRedis(
                host= "localhost",
                port= 6379,
                password= 1234,
                db= 0,
                decode_responses=True
            )
            self.logger.info("Redis 连接成功")
        except redis.RedisError as e:
            self.logger.error(f"Redis 连接失败: {e}")
            raise

    def set_data(self, key, value):
        try:
            self.client.set(key, json.dumps(value))
            self.logger.info(f"存储数据到 Redis: {key}")
        except redis.RedisError as e:
            self.logger.error(f"Redis 存储失败: {e}")

    def get_data(self, key):
        try:
            data = self.client.get(key)
            return json.loads(data) if data else None
        except redis.RedisError as e:
            self.logger.error(f"Redis 获取失败: {e}")
            return None

    def get_answer(self, query):
        try:
            answer = self.client.get(f"answer:{query}")
            if answer:
                self.logger.info(f"从 Redis 获取答案: {query}")
                return answer
            return None
        except redis.RedisError as e:
            self.logger.error(f"Redis 查询失败: {e}")
            return None

def main():
    # 初始化 Redis 客户端
    redis_client = RedisClient()
    # 示例数据
    key = "answer:user1"
    value = {"name": "Alice", "age": 25}
    # 存储数据
    redis_client.set_data(key, value)
    # 获取数据
    result = redis_client.get_data(key)
    if result:
        logger.info(f"查询结果: {result}")
    else:
        logger.info("未找到数据")
    # 示例查询缓存
    query = "user1"
    answer = redis_client.get_answer(query)
    if answer:
        logger.info(f"缓存答案: {answer}")
    else:
        logger.info("未找到缓存答案")

if __name__ == "__main__":
    main()
