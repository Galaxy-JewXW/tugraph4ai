from langchain.prompts import ChatPromptTemplate
import json

from rag import *
from setting import *

def _get_llm() :
    from llm.ChatOpenAI import get_ChatOpenAI
    llm = get_ChatOpenAI()

    return llm

def conclude(question, answer, verbose=False):
    PROMPT_TEMPLATE = """
    对问题的答案进行概括，给出一个更简要的答案。
    如果你觉得原始答案已经足够简洁，也可以不进行概括。
    问题是：
    {question}
    ---
    答案是：
    {answer}
    ---
    直接给出概括后的答案
    """

    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

    chat_llm_chain = LLMChain(
        llm= _get_llm(),
        prompt=prompt,
        verbose=verbose, # 是否显示Token
    )

    # 生成回复
    res = chat_llm_chain.predict(
        question=question,
        answer=answer
    )

    return res

def _answer_problem(problem_file, result_file):
    rag = RAG()

    results = []
    with open(problem_file, "r") as file:
        for line in file:
            data = json.loads(line)
            question = data["input_field"]

            result = rag.search(question)
            result_conclude = conclude(question, result)
            results.append({
                "id": data["id"],
                "output_field": result_conclude
            })

            print(f"[answer]: \n"
                  f"\tquestion is: {question}: \n"
                  f"\tanswer   is: {result}\n"
                  f"\tconclude is: {result_conclude}\n")
            print("##################################\n\n")

    # 将提取的数据写入到answer.jsonl文件中
    with open(result_file, "w", encoding="utf-8") as f:
        for result in results:
            # 将每个字典转换为JSON格式的字符串，并写入文件
            json_line = json.dumps(result, ensure_ascii=False) + "\n"
            f.write(json_line)
    print(f"[answer]: 数据已写入到{result_file}文件中")


def answer_question():
    _answer_problem("data/test1.jsonl", "result/answer.jsonl")
    _answer_problem("data/val.jsonl", "result/test_ans.jsonl")


if __name__ == "__main__":
    answer_question()
