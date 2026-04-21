# coding: utf-8
# 导包
from rank_bm25 import BM25Okapi # BM25算法
import numpy as np # 数值计算库

import os, sys
# 路径
current_dir_path = os.path.dirname(os.path.abspath(__file__))
module_dir_path = os.path.dirname(current_dir_path)
project_path = os.path.dirname(module_dir_path)
sys.path.insert(0, module_dir_path) # 添加模块目录
sys.path.insert(0, project_path)    # 添加根目录

from utils.preprocess import preprocess_text    # 处理文本
from db.mysql_client import MySQLClient         # mysql client
from cache.redis_client import RedisClient   # redis client
from base import logger, Config                 # 日志， config配置


# 创建类BM25Search
class BM25Search():
    # init
    def __init__(self, redis_client, mysql_client):
        self.logger = logger                # 日志
        self.redis_client = redis_client    # redis客户端
        self.mysql_client = mysql_client    # mysql客户端

        self.bm25 = None                    # bm25模型
        self.questions = None               # 初始化问题列表
        self.original_questions = None      # 初始化原始问题
        self._load_data()                   # 加载数据

    # _loda_data方法
    def _load_data(self):
        # 加载数据
        original_key = "qa_original_questions"
        tokenized_key = "qa_tokenized_questions"
        # 从redis中获取原始问题答案
        self.original_questions = self.redis_client.get_data(original_key)
        # 从redis中获取分词后的问题答案
        tokenized_questions = self.redis_client.get_data(tokenized_key)
        # 如果redis没有从，从Mysql中加载
        if not self.original_questions or not tokenized_questions:
            self.original_questions = self.mysql_client.fetch_questions()
            if not self.original_questions:
                self.logger.warning("未加载问题")
                return
            # 对问题分词
            tokenized_questions = [preprocess_text(q[0]) for q in self.original_questions]
            # 将分词前后的问题存储到redis里面
            self.redis_client.set_data(original_key, [q[0] for q in self.original_questions])
            self.redis_client.set_data(original_key, tokenized_questions)

        # 设置问题列表
        self.questions = tokenized_questions
        # 初始化BM25模型
        self.bm25 = BM25Okapi(self.questions)
        # 记录BM25初始化成功
        self.logger.info("BM25 模型初始化成功")

    # 定义softmax方法
    def _softmax(self, scores):
        # 计算softmax分数，但是我们对每个score都减去一个最大值，为了防止数据过大，内存爆炸
        exp_scores = np.exp(scores - np.max(scores))
        # 返回归一化分数
        return exp_scores/ exp_scores.sum()

    # 定义search方法，实现查询
    def search(self, query, threshold=0.85):
        # 搜索查询
        if not query or not isinstance(query, str):
            # 记录无效查询
            self.logger.error("无效查询")
            return None, False
        # 检查redis缓存
        cached_answer = self.redis_client.get_answer(query)
        if cached_answer:
            return cached_answer, False
        try:
            # 分词
            query_tokens = preprocess_text(query)
            # 计算bm25的分数
            scores = self.bm25.get_scores(query_tokens)
            # 对分数归一化
            softmax_score = self._softmax(scores)
            # 获取分数最高的索引
            best_idx = softmax_score.argmax()
            # 根据上述索引获得最高分值
            best_score = softmax_score[best_idx]
            # 判断分数是否超过阈值
            if best_score >= threshold:
                # 原始问题
                original_question = self.original_questions[best_idx]
                # 查数据库获得问题对应的答案
                answer = self.mysql_client.fetch_answer(original_question)
                if answer:
                    # 缓存qa对
                    self.redis_client.set_data(f'answer:{query}', answer)
                    # 记录搜索成功
                    self.logger.info(f"搜索成功， softmax相似度:{best_score:.3f}")
                    return answer, False
            # 如果分数没有超过阈值，记录无可靠答案
            self.logger.info(f"为找到可靠答案，最高 softmax 相似度:{best_score: .3f}")
            return None, True
        except Exception as e:
            self.logger.error(f'搜索失败:{e}')
            return None, True

if __name__ == '__main__':
    redis_client = RedisClient()
    mysql_client = MySQLClient()
    bm25_search = BM25Search(redis_client, mysql_client)
    print(bm25_search.search(query="VMware安装VMware时显示灰色如何解决"))