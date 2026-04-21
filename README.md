# EduRAG

教育问答系统 | RAG + MySQL + Redis + Milvus

## 项目简介

EduRAG 是一个基于 RAG（检索增强生成）架构的教育领域问答系统，支持多学科知识检索、流式答案输出和多轮对话管理。

## 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                      前端 (Vue 3)                       │
│              http://localhost:3000                       │
└────────────────────────┬────────────────────────────────┘
                         │ SSE
┌────────────────────────▼────────────────────────────────┐
│                   FastAPI 后端                           │
│                  http://localhost:8000                  │
│  ┌─────────────┬──────────────┬────────────────────────┐ │
│  │ RAGSystem   │ MySQLClient  │  RedisClient (BM25)    │ │
│  └─────────────┴──────────────┴────────────────────────┘ │
│         │                                      │        │
│  ┌──────▼──────┐                         ┌────▼─────┐   │
│  │   Milvus    │                         │  MySQL   │   │
│  │ (向量存储)   │                         │ (结构化) │   │
│  └─────────────┘                         └──────────┘   │
└─────────────────────────────────────────────────────────┘
```

## 目录结构

```
EduRAG/
├── edu-rag-frontend/       # Vue 3 前端应用
│   ├── src/
│   │   ├── App.vue        # 主组件
│   │   └── main.js        # 入口文件
│   └── vite.config.js     # Vite 配置
├── integrated_qa_system/  # FastAPI 后端
│   ├── api.py             # API 入口
│   ├── new_main.py        # 集成问答系统
│   ├── mysql_qa/          # MySQL + Redis 模块
│   │   ├── cache/         # Redis 缓存
│   │   ├── db/            # MySQL 客户端
│   │   └── retrieval/     # BM25 检索
│   └── rag_qa/            # RAG 核心模块
│       ├── core/          # RAG 系统核心
│       │   ├── rag_system.py
│       │   ├── vector_store.py
│       │   ├── query_classifier.py  # BERT 查询分类
│       │   └── strategy_selector.py  # 检索策略选择
│       ├── edu_document_loaders/     # 文档加载
│       └── edu_text_spliter/         # 文本分块
└── docs/                  # 项目文档
```

## 核心功能

- **RAG 检索增强**：结合向量检索（Milvus）与 BM25 混合检索
- **多学科分类**：支持 AI、Java、Test、Ops、BigData 等学科过滤
- **流式输出**：SSE 流式响应，实时逐字显示答案
- **多轮对话**：维护会话历史，支持上下文理解
- **文档解析**：支持 PDF、PPT、Word、图片等多格式文档
- **查询分类**：基于 BERT 的智能查询分类，自动选择检索策略

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Redis 7.0+
- Milvus 2.4+（可选）

### 后端部署

```bash
cd integrated_qa_system

# 安装依赖
pip install -r requirements.txt

# 配置环境变量（设置 DashScope API Key）
# 编辑 base/config.py 或设置环境变量

# 启动服务
python api.py
```

### 前端部署

```bash
cd edu-rag-frontend

# 安装依赖
npm install

# 开发模式
npm run dev

# 生产构建
npm run build
```

### API 接口

**POST /query** - 问答接口（SSE 流式响应）

```json
{
  "query": "什么是人工智能？",
  "source_filter": "ai",
  "session_id": "可选的会话ID"
}
```

响应格式：
```
data: {"token": "这", "is_complete": false, "session_id": "xxx"}\n\n
data: {"token": "是", "is_complete": false, "session_id": "xxx"}\n\n
...
data: {"token": "答案完成", "is_complete": true, "session_id": "xxx"}\n\n
```

## 技术栈

| 组件 | 技术 |
|------|------|
| 前端框架 | Vue 3 + Vite |
| 后端框架 | FastAPI + Uvicorn |
| 向量数据库 | Milvus |
| 关系数据库 | MySQL 8.0 |
| 缓存 | Redis |
| LLM API | DashScope (通义千问) |
| Embedding | BGE-M3 / BERT |
| Reranker | BGE-Reranker |

## 注意事项

- 模型文件（`rag_qa/models/`）体积较大，通过 `.gitignore` 排除版本管理
- 首次运行需要配置 DashScope API Key
- Milvus 为可选组件，不启动时系统使用基础检索模式