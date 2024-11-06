from langchain_openai import ChatOpenAI
from setting import *

def get_ChatOpenAI():
    llm = ChatOpenAI(
        model_name=LLM_MODEL_NAME,
        openai_api_base=LLM_API_BASE,
        openai_api_key=LLM_API_KEY,
        streaming=False,
    )

    return llm