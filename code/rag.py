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

class RAG:
    def __init__(self, retriver, llm):
        self.retriver = retriver
        self.llm = llm
        self.memory = []

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
        # 如果是Qwen改为"content"，否则为"question"
        # 注意一起修改上面的prompt
        rewrite = llm_chain.invoke({"question": question}).content
        # qwen后面不需要.content
        # rewrite = llm_chain.invoke({"content": question})

        print(f"[rewrite: ] \n\tinit is {question} \n\tnow is {rewrite}\n")
        return rewrite

    def get_context(self, question, score_threshold=0):
        # 对问题进行改写
        question = self._rewrite_question(question)

        # 余弦相似度召回
        docs = self.retriver.invoke(question)

        # 重排
        tokenizer = AutoTokenizer.from_pretrained(self.config.rerank_model)
        model = AutoModelForSequenceClassification.from_pretrained(self.config.rerank_model)
        model.eval()

        pairs = [[question, doc.page_content] for doc in docs]
        with torch.no_grad():
            inputs = tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
            scores = model(**inputs, return_dict=True).logits.view(-1, ).float()
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

    def search(self, question):
        context = self.get_context(question)

        PROMPT_TEMPLATE = """以下是历史聊天记录:
        {chat_history}
        ---
        以下是参考信息：
        {context}
        ---
        以下是我当前的问题：
        {question}
        ---
        请根据上述聊天记录和参考信息回答我当前的问题。前面的聊天记录和参考信息可能有用，也可能没用，你需要从我给出的参考信息中选出与我的问题最相关的那些，来为你的回答提供依据。回答一定要忠于原文，简洁但不丢信息，不要胡乱编造。请给出回答。"""

        prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

        chat_llm_chain = LLMChain(
            llm=self.llm,
            prompt=prompt,
            verbose=True,
        )

        # 生成回复
        res = chat_llm_chain.predict(
            # 格式化聊天记录为JSON字符串
            chat_history = "\n".join([f"{entry['role']}: {entry['content']}" for entry in self.memory]),
            # chat_history = "\n".join(self.memory),
            context=context,
            question=question
        )

        # 更新聊天历史
        self.memory.append({'role': 'user', 'content': question})
        self.memory.append({'role': 'assistant', 'content': res})
