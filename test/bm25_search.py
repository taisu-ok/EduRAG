import jieba
from rank_bm25 import BM25L


class BM25Search:
    def __init__(self, documents):
        # 初始化文档集合
        self.documents = documents
        # 分词后的文档
        self.tokenized_docs = [jieba.lcut(doc) for doc in documents]
        # 初始化BM25模型
        self.bm25 = BM25L(self.tokenized_docs)

    def search(self, query):
        # 分词查询
        tokenized_query = jieba.lcut(query)
        try:
            # 计算每个文档的BM25得分
            scores = self.bm25.get_scores(tokenized_query)
            print(f'scores--》{scores}')
            # 获取最高得分的文档索引
            best_idx = scores.argmax()
            best_score = scores[best_idx]
            best_doc = self.documents[best_idx]
            return best_doc, best_score
        except Exception as e:
            return None, 0.0


def main():
     # 示例文档集合
     documents = ["我喜欢编程", "编程很有趣"]
     # 初始化BM25检索器
     bm25_search = BM25Search(documents)
     # 示例查询
     query = "他喜欢编程"
     # 执行检索
     result, score = bm25_search.search(query)
     print(f'Result: {result}, Score: {score}')

if __name__ == '__main__':
    main()
