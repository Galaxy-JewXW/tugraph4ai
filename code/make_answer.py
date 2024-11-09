import os
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.retrievers.bm25 import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
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
from make_embedding import get_docs

def _format_docs(docs):
    return "\n".join(doc.page_content for doc in docs)

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

# 获取检索器
def _get_embedding_retriever():
    embedding_model = _get_embedding_model()

    # 用于存储和检索文档的嵌入向量
    db = FAISS.load_local(
        f"data/{EMBEDDING_DB_NAME}",
        embedding_model,
        allow_dangerous_deserialization=True,
    )
    retriever = db.as_retriever(search_kwargs={"k": SEARCH_NUM})

    # 如果不需要混合分词，则取消注释
    # return retriever

    # 重新生成docs耗时过久
    docs = get_docs()
    bm25_retriever = BM25Retriever.from_documents(
        docs,
        k=SEARCH_NUM,
        bm25_params={"k1": 1.5, "b": 0.75},
        preprocess_func=jieba.lcut  # 中文需要使用jieba分词
    )
    ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, retriever], weights=[0.4, 0.6])

    return ensemble_retriever

def _get_llm() :
    from llm.ChatOpenAI import get_ChatOpenAI
    llm = get_ChatOpenAI()

    # from llm.Qwen import get_Qwen_local
    # llm = get_Qwen_local()

    return llm

def _get_rag():
    # 获取检索器
    retriever = _get_embedding_retriever()
    # 加载了一个提示模板
    prompt = hub.pull("rlm/rag-prompt")
    # 加载LLM

    llm = _get_llm()

    # 从文档中查找答案
    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: _format_docs(x["context"])))
        | prompt  # 管道操作
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel({
        "context": retriever,
        "question": RunnablePassthrough()
    }).assign(answer=rag_chain_from_docs)

    return rag_chain_with_source

# 传入原始的question，进行改写，使得更加规划
def _rewrite_question(question):
    prompt_template = """
        现在我需要问你关于TuGraph-DB问题：
        {question}
        ---
        原始的问题可能是简略的、口语化的、不完整的。
        请根据下列指示改写我的问题：将原始问题转换为更加明确、简洁，并针对性强的形式，以便于在数据库或搜索引擎中进行有效检索。
        请直接给出改写后的问题。
        """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    llm = _get_llm()

    llm_chain = prompt | llm
    # 如果是Qwen改为"content"，否则为"question"
    # 注意一起修改上面的prompt
    rewrite = llm_chain.invoke({"question": question}).content
    # qwen后面不需要.content
    # rewrite = llm_chain.invoke({"content": question})

    print(f"[rewrite: ] \n\tinit is {question} \n\tnow is {rewrite}\n")
    return rewrite

def _answer_problem(problem_file, result_file):
    rag = _get_rag()

    results = []
    with open(problem_file, "r") as file:
        for line in file:
            data = json.loads(line)
            question = data["input_field"]
            rewrite = _rewrite_question(data["input_field"])

            result = rag.invoke(rewrite)
            results.append({
                "id": data["id"],
                "output_field": result["answer"]
            })

            print(f"[answer]: \n\tquestion is: {question}: \n\tanswer is: {result['answer']}")
            print("##################################\n\n")

    # 将提取的数据写入到answer.jsonl文件中
    with open(result_file, "w", encoding="utf-8") as f:
        for result in results:
            # 将每个字典转换为JSON格式的字符串，并写入文件
            json_line = json.dumps(result, ensure_ascii=False) + "\n"
            f.write(json_line)
    print(f"[answer]: 数据已写入到{result_file}文件中")


def answer_question():
    # _answer_problem("data/test1.jsonl", "result/answer.jsonl")
    _answer_problem("data/val.jsonl", "result/test_ans.jsonl")


if __name__ == "__main__":
    answer_question()
