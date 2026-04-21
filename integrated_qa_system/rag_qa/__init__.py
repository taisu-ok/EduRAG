# 添加系统路径
import os, sys
rag_qa_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, rag_qa_path)

# 导包
from core.vector_store import VectorStore
from core.new_rag_system import RAGSystem


