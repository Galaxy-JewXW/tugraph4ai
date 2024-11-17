SUCCESS_URL_FILE = "data/successful_urls.txt"

# 查询向量库时返回的文本数量
SEARCH_NUM = 9

# 每个文本块的最大字符数
CHUNK_SIZE = 2048
# 相邻文本块之间的重叠字符数
CHUNK_OVERLAP = 512

# embedding向量库的地址
EMBEDDING_DB_NAME = f"embedding_{CHUNK_SIZE}_{CHUNK_OVERLAP}"

# 用于将文档转换为向量库的模型名
EMBEDDING_MODEL_NAME = "BAAI/bge-large-zh-v1.5"
# 用于重排的模型名
RERANKER_MODEL_NAME = "BAAI/bge-reranker-large"
# 用于计算相似度的SOTA模型
SOTA_SIMILARITY_NAME = "BAAI/bge-large-zh-v1.5"

# 用于问答的LLM
LLM_MODEL_NAME = "GLM-4-PLus"
LLM_API_BASE = "https://open.bigmodel.cn/api/paas/v4"
LLM_API_KEY = "put your key here"

# Qwen选取的模型型号
QWEN_NAME = "qwen/Qwen1.5-7B-Chat"
QWEN_ADDR = "/root/workshop/model/Qwen1.5-7B-Chat"
QWEN25_NAME = "qwen/Qwen2.5-7B"