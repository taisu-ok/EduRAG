# class A():
#     def a1(self):
#         print('你好A')
#     def b1(self):
#         self.a1()
#
# class B(A):
#     def a1(self,):
#         print('你好B')
#
# b = B()
# b.b1()


# from transformers import BertModel
# bert_model = BertModel.from_pretrained('/Users/ligang/Desktop/EduRAG课堂资料/codes/integrated_qa_system/rag_qa/nlp_bert_document-segmentation_chinese-base')
# print(bert_model)

import os


def get_modelscope_cache_dir():
    # 优先读取自定义环境变量 MODELSCOPE_HUB_HOME
    custom_dir = os.getenv("MODELSCOPE_HUB_HOME")
    if custom_dir:
        return os.path.join(custom_dir, "hub")

    # 无自定义路径，返回默认路径
    home_dir = os.path.expanduser("~")  # 获取用户主目录（C:\Users\35090\）
    default_dir = os.path.join(home_dir, ".cache", "modelscope", "hub")
    return default_dir


# 打印模型下载根目录
model_cache_dir = get_modelscope_cache_dir()
print("ModelScope 模型下载根目录：", model_cache_dir)

# 打印你下载的模型具体路径
your_model_path = os.path.join(model_cache_dir, "iic", "nlp_bert_document-segmentation_chinese-base")
print("你的模型具体存放路径：", your_model_path)