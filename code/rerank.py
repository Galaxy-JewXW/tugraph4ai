from langchain_community.retrievers.bm25 import BM25Retriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from setting import *

def rerank(docs, question):
    import jieba
    retriever = BM25Retriever.from_documents(
        docs, 
        k=10,
        bm25_params={"k1": 1.5, "b": 0.75}, 
        preprocess_func=jieba.lcut
    )
    ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, dense_retriever], weights=[0.4, 0.6])
    
    rerank_model = HuggingFaceCrossEncoder(model_name=RERANKER_MODEL_NAME)
    
    compressor = CrossEncoderReranker(model=rerank_model, top_n=top_n)
    compression_retriever = ContextualCompressionRetriever(
        base_compressor=compressor, base_retriever=retriever
    )
    rerank_answers = []
    for question in tqdm(questions):
        relevant_docs = compression_retriever.invoke(question)
        answer=''
        for rd in relevant_docs:
            answer += rd.page_content
        rerank_answers.append(answer[:245])
    return rerank_answers