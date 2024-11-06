from langchain.prompts import ChatPromptTemplate
import json

from rag import *
from setting import *

def _answer_problem(problem_file, result_file):
    rag = RAG()

    results = []
    with open(problem_file, "r") as file:
        for line in file:
            data = json.loads(line)
            question = data["input_field"]

            result = rag.search(question)
            results.append({
                "id": data["id"],
                "output_field": result
            })

            print(f"[answer]: \n\tinit is: {question}: \n\tanswer is: {result}")
            print("##################################")

    # 将提取的数据写入到answer.jsonl文件中
    with open(result_file, "w", encoding="utf-8") as f:
        for result in results:
            # 将每个字典转换为JSON格式的字符串，并写入文件
            json_line = json.dumps(result, ensure_ascii=False) + "\n"
            f.write(json_line)
    print(f"[answer]: 数据已写入到{result_file}文件中")


def answer_question():
    _answer_problem("data/test1.jsonl", "result/rag_answer.jsonl")
    _answer_problem("data/val.jsonl", "result/rag_test_ans.jsonl")


if __name__ == "__main__":
    answer_question()
