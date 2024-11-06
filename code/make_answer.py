from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers.bm25 import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain_openai import ChatOpenAI
from FlagEmbedding import FlagReranker
import pandas as pd
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableParallel
from langchain.retrievers import ContextualCompressionRetriever
import json
import jieba

from setting import *


def _format_docs(docs):
    return "".join(doc.page_content for doc in docs)


def _get_embedding_model():
    model_name = EMBEDDING_MODEL_NAME
    model_kwargs = {"device": "cuda"}
    # 对嵌入向量进行归一化处理
    encode_kwargs = {"normalize_embeddings": True}
    # 创建了一个用于生成句子嵌入的实例，用于数据库检索
    embedding_model = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
        query_instruction="为这个句子生成表示以用于检索相关文章:",
    )
    return embedding_model


def _get_reranker():
    reranker = FlagReranker(
        RERANKER_MODEL_NAME, use_fp16=True
    )  # Setting use_fp16 to True speeds up
    return reranker

# 获取检索器
def _get_embedding_retriever():
    embedding_model = _get_embedding_model()

    # 用于重排检索结果的实例
    # reranker = _get_reranker()

    # 用于存储和检索文档的嵌入向量
    db = FAISS.load_local(
        f"data/{EMBEDDING_DB_NAME}",
        embedding_model,
        allow_dangerous_deserialization=True,
    )
    retriever = db.as_retriever(search_kwargs={"k": SEARCH_NUM})
    
    bm25_retriever = BM25Retriever.from_documents(
        docs, 
        k=5, 
        bm25_params={"k1": 1.5, "b": 0.75}, 
        preprocess_func=jieba.lcut
    )
    ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, retriever], weights=[0.4, 0.6])
    
    return ensemble_retriever


def _get_rag():
    # 获取检索器
    retriever = _get_embedding_retriever()
    # 加载了一个提示模板
    prompt = hub.pull("rlm/rag-prompt")
    # 加载LLM
    llm = ChatOpenAI(
        model_name=LLM_MODEL_NAME,
        openai_api_base=LLM_API_BASE,
        openai_api_key=LLM_API_KEY,
        streaming=False,
    )

    # 从文档中查找答案
    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: _format_docs(x["context"])))
        | prompt  # 管道操作
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    return rag_chain_with_source


def _answer_problem(problem_file, result_file):
    rag = _get_rag()

    results = []
    with open(problem_file, "r") as file:
        for line in file:
            data = json.loads(line)
            question = data["input_field"]
            # prompt = (
            #     "以下问题只关于TuGraph-DB\n"
            #     + question
            #     + "\n要求：直接回答结果，如果不知道回答不知道，不要添加额外内容，不要进行推测。回答长度不要超过100字。"
            # )
            result = rag.invoke(question)
            results.append({"id": data["id"], "output_field": result["answer"]})

            print(f"[answer]: {question}: {result['answer']}")

    # 将提取的数据写入到answer.jsonl文件中
    with open(result_file, "w", encoding="utf-8") as f:
        for result in results:
            # 将每个字典转换为JSON格式的字符串，并写入文件
            json_line = json.dumps(result, ensure_ascii=False) + "\n"
            f.write(json_line)
    print(f"[answer]: 数据已写入到{result_file}文件中")


def answer_question():
    _answer_problem("data/test1.jsonl", "result/test_ans.jsonl")
    _answer_problem("data/val.jsonl", "result/answer.jsonl")


if __name__ == "__main__":
    answer_question()
