# coding:utf-8
# 导包
import pymysql  # mysql连接
import pandas as pd
import sys, os

# 路径，让路径在终端，linux可用
current_dir_path = os.path.dirname(os.path.abspath(__file__))   # 获取当前目录路径
module_path = os.path.dirname(current_dir_path)   # 当前根目录
project_root = os.path.dirname(module_path) # 当前根目录

# 添加根目录
sys.path.insert(0, project_root)
from base import Config, logger


# 定义MySQLClient类
class MySQLClient:
    def __init__(self):
        # 初始化日志
        self.logger = logger
        try:
            # 连接MySQL数据库
            self.connection = pymysql.connect(
                host=Config().MYSQL_HOST,
                user=Config().MYSQL_USER,
                password=Config().MYSQL_PASSWORD,
                database=Config().MYSQL_DATABASE
            )
            # 创建游标
            self.cursor = self.connection.cursor()
            # 记录连接成功
            self.logger.info("MySQL 连接成功")

        except pymysql.MySQLError as e:
            self.logger.error(f'MySQL 连接失败: {e}')
            raise


    # 创建表
    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS jpkb(
            id INT AUTO_INCREMENT PRIMARY KEY,
            subject_name VARCHAR(20),
            question VARCHAR(1000),
            answer VARCHAR(1000)
        )
        """
        try:
            self.cursor.execute(create_table_query)
            self.connection.commit()
            self.logger.info("表创建成功")
        except pymysql.MySQLError as e:
            self.logger.error(f"表创建失败:{e}")
            raise

    # 添加数据
    def insert_data(self, csv_path):
        try:
            data = pd.read_csv(csv_path)
            for _,row in data.iterrows():
                insert_query = "INSERT IGNORE INTO jpkb (subject_name, question, answer) VALUES (%s, %s, %s)"
                self.cursor.execute(insert_query, (row["学科名称"], row["问题"], row['答案']))
            self.connection.commit()
            self.logger.info("Mysql数据插入成功")
        except pymysql.MySQLError as e:
            self.logger.error(f'Mysql数据插入失败:{e}')
            self.connection.rollback()
            raise

    # 获取所有问题
    def fetch_questions(self):
        try:
            self.cursor.execute("SELECT question FROM jpkb")
            # 获取结果
            result = self.cursor.fetchall()
            self.logger.info("成功获取问题")
            return result
        except pymysql.MySQLError as e:
            self.logger.error(f"查询失败:{e}")
            # 返回空列表
            return []

    # 获取指定问题答案
    def fetch_answer(self, question):
        try:
            self.cursor.execute("SELECT answer FROM jpkb WHERE question=%s", (question,))
            # 获取结果
            result = self.cursor.fetchone()
            self.logger.info("成功查询问题")
            return result[0] if result else None
        except pymysql.MySQLError as e:
            self.logger.error(f'答案获取失败: {e}')
            return None

    # 关闭数据库连接
    def close(self):
        try:
            self.connection.close()
            # 日志记录
            self.logger.info("Mysql 连接已关闭")
        except pymysql.MySQLError as e:
            self.logger.error(f'关闭连接失败:{e}')


if __name__ == '__main__':
    client = MySQLClient()
    # client.create_table()
    # client.insert_data(csv_path='../data/JP学科知识问答.csv')
    quetions = client.fetch_questions()
    print(quetions)
    ans = client.fetch_answer(question="用上下文管理器实现函数运行时间的计算?")
    print(ans)
    client.close()