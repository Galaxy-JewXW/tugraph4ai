import os

os.environ["USER_AGENT"] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.text_splitter import (
    CharacterTextSplitter,
    RecursiveCharacterTextSplitter,
)
from langchain_community.document_loaders import TextLoader, WebBaseLoader
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableParallel
from langchain_community.document_loaders import PyPDFDirectoryLoader

from setting import *


def _get_crawl_urls(filename=None) -> dict:
    if filename is None:
        raise Exception("no crawl urls")

    # 读取successful_urls.txt中的所有链接
    with open(filename, "r") as file:
        # 假设每一行是一个链接，strip()去除换行符
        successful_urls = [line.strip() for line in file.readlines()]

    # 合并并去重 manual_links, all_links, 和 successful_urls
    all_links = list(set(successful_urls))
    print(f"the total len of crawl urls is: {len(all_links)}")

    return all_links

def _get_contents(urls):
    loader = WebBaseLoader(urls)
    documents = loader.load()

    separators = ["\n\n", "\n", " ", ".", ",", "，", "。",]  # 定义分割符
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,  # 每个文本块的最大字符数
        chunk_overlap=CHUNK_OVERLAP,  # 相邻文本块之间的重叠字符数
        separators=separators,  # 用于识别文本块边界的分割符
        keep_separator=False,  # 是否保留这些分割符在文本块中
    )
    documents = text_splitter.split_documents(documents)
    return documents

def get_docs():
    crawl_file = "data/successful_urls.txt"
    urls = _get_crawl_urls(crawl_file)
    documents = _get_contents(urls)
    return documents

def _get_embedding_model():
    model_name = EMBEDDING_MODEL_NAME
    model_kwargs = {"device": "cuda"}
    # 当向量都被规范化（归一化）后，它们的范数都是1。
    # 余弦相似度的计算只需要向量的点积运算，从而减少了计算的复杂度，加快了处理速度。
    encode_kwargs = {"normalize_embeddings": True}
    embedding = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
        query_instruction="为这个句子生成表示以用于检索相关文章："
    )
    return embedding

def _create_db(documents, embedding):
    # AISS在高效相似度搜索和GPU加速方面表现出色
    # ChromaDB则提供了全面的数据库功能和分布式处理能力
    db = FAISS.from_documents(
        documents, 
        embedding=embedding
    )
    db.save_local(f"data/{EMBEDDING_DB_NAME}")

    return db

def make_embedding_db():
    # 获取原先的爬取的网页文档
    crawl_file = "data/successful_urls.txt"
    urls = _get_crawl_urls(crawl_file)
    print(f"[embedding]: get crawl urls successful")

    # 将提取到的子页面分解为更小的文本块
    documents = _get_contents(urls)
    print(f"[embedding]: convert urls to documents successful")

    # 将文本转换为向量化实例
    embedding_model = _get_embedding_model()
    print(f"[embedding]: get embedding model")

    # 使用FAISS库创建一个向量数据库，它将存储从文档中提取的嵌入向量
    db = _create_db(documents, embedding_model)
    print(f"[embedding]: embedding successful!!!")
    print(f"[embedding]: !!!!!!!!!!!!!!!!!!!!!!!\n\n")
    return db

if __name__ == "__main__":
    # 基于爬虫文档创建向量数据库
    db = make_embedding_db()

    # 检索时返回的相关文档数量
    search_num = SEARCH_NUM
    retriever = db.as_retriever(search_kwargs={"k": search_num})

    print(
        retriever.get_relevant_documents(
            "RPC 及 HA 服务中，verbose 参数的设置有几个级别？"
        )
    )
    print(
        retriever.get_relevant_documents(
            "`FieldData` 类中的函数 `IsReal()` 是用来查询什么类型的数据？"
        )
    )
