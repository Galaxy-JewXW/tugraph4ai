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
from langchain_community.document_transformers import LongContextReorder
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import jieba

from make_embedding import get_docs
from setting import *

class RAG:
    def __init__(self):
        self.retriver = _get_embedding_retriever()
        self.llm = _get_llm()

        self.tokenizer = AutoTokenizer.from_pretrained(RERANKER_MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(RERANKER_MODEL_NAME)
        self.model.eval()

    def _rewrite_question(self, question):
        prompt_template = """
            现在我需要问你关于TuGraph-DB问题：
            {question}
            ---
            原始的问题可能是简略的、口语化的、不完整的。
            请根据下列指示改写我的问题：将原始问题转换为更加明确、简洁，并针对性强的形式，以便于在数据库或搜索引擎中进行有效检索。
            请直接给出改写后的问题。
            """
        prompt = ChatPromptTemplate.from_template(prompt_template)

        llm_chain = prompt | self.llm
        rewrite = llm_chain.invoke({"question": question}).content

        print(f"[rewrite: ] \n\tinit is {question} \n\tnow is {rewrite}\n")
        return rewrite

    def get_context(self, question, score_threshold=0):
        # 对问题进行改写
        question = self._rewrite_question(question)

        # 余弦相似度召回
        docs = self.retriver.invoke(question)

        # 重排
        pairs = [[question, doc.page_content] for doc in docs]
        with torch.no_grad():
            inputs = self.tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
            scores = self.model(**inputs, return_dict=True).logits.view(-1, ).float()
        # 确保scores是一维的
        scores = scores.squeeze()
        # 将docs和scores组合成一个列表
        doc_scores = list(zip(docs, scores.tolist()))
        # 对文档进行排序，基于得分从高到低
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        # 提取排序后的文档对象，阈值过滤
        sorted_docs = [doc for doc, score in doc_scores if score >= score_threshold]
        # 长上下文检索器，将最相关的文档放在开始和结尾，中间放无关紧要的
        reordering = LongContextReorder()
        reordered_docs = reordering.transform_documents(sorted_docs)

        return "\n\n".join(doc.page_content for doc in reordered_docs)

    def search(self, question, verbose=False):
        context = self.get_context(question)

        PROMPT_TEMPLATE = """
        As a specialized AI assistant for question-answering, I will use the given context to provide a clear and concise response to your query in no more than three sentences, without adding any LLM-specific filler words such as '好的' or '从资料中可以得出'. If the necessary information is not available, I will let you know. 
        Aanswer in a brief way.
        Context: 
        {context}
        ---
        Question:
        {question}
        ---
        Here is your answer:
        """

        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

        chat_llm_chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            verbose=verbose, # 是否显示Token
        )

        # 生成回复
        res = chat_llm_chain.predict(
            context=context,
            question=question
        )

        return res

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

    # 用于重排检索结果的实例
    # reranker = _get_reranker()

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
    ensemble_retriever = EnsembleRetriever(
                            retrievers=[bm25_retriever, retriever], 
                            weights=[0.4, 0.6])

    return ensemble_retriever

def _get_llm() :
    from llm.ChatOpenAI import get_ChatOpenAI
    llm = get_ChatOpenAI()

    # from llm.Qwen import get_Qwen_local
    # llm = get_Qwen_local()

    return llm
  
if __name__ == "__main__":
    rag = RAG()
    print(rag.search("当前图数据库应用程序使用的CPU比率是多少？", verbose=True))