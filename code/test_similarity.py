from sentence_transformers import SentenceTransformer, util
import torch
import json

from setting import *

def get_similarity(sen1: str, sen2: str):
    # 加载预训练模型
    model = SentenceTransformer(model_name_or_path=SOTA_SIMILARITY_NAME)

    # 将句子转换为句子嵌入
    embedding1 = model.encode(sen1, convert_to_tensor=True)
    embedding2 = model.encode(sen2, convert_to_tensor=True)

    # 计算两个句子嵌入之间的余弦相似度
    cosine_similarity = util.pytorch_cos_sim(embedding1, embedding2)
    similarity_score = (cosine_similarity.item() + 1) / 2

    # print("归一化的相似度分数:", similarity_score)
    return similarity_score

def compute_val(result_dir='result/'):
    # 定义文件路径
    file_ans = 'data/val.jsonl'
    file_result = result_dir + 'test_ans.jsonl'

    # 初始化字典存储文件1和文件2的输出字段
    outputs_ans = {}
    outputs_res = {}

    # 读取第一个文件并存储输出字段
    with open(file_ans, 'r', encoding='utf-8') as file1:
        for line in file1:
            data = json.loads(line)
            outputs_ans[data['id']] = data['output_field']

    # 读取第二个文件并存储输出字段
    with open(file_result, 'r', encoding='utf-8') as file2:
        for line in file2:
            data = json.loads(line)
            outputs_res[data['id']] = data['output_field']

    total_similarity = 0
    count = 0

    error_list = []
    for id, output1 in outputs_ans.items():
        if id in outputs_res:
            output2 = outputs_res[id]

            # 累加相似度
            similarity = get_similarity(output1, output2)
            total_similarity += similarity
            count += 1

            print(f"{similarity}\t{id}:\n\t{output1}\n\t{output2}\n")
            if similarity < 0.7:
                error_list.append((id, similarity, output1, output2))

    # 计算平均相似度
    average_similarity = total_similarity / count if count > 0 else 0

    error_list = sorted(error_list, key=lambda x: x[1])
    output_file = result_dir + 'error_similar.log'
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for item in error_list:
            content = f"ID: {item[0]}, 相似度: {item[1]}:\n\t{item[2]}\n\t{item[3]}\n\n"
            print(content)
            outfile.write(content)
        outfile.write(f"\n平均余弦相似度: {average_similarity}\n")

if __name__ == "__main__":
    compute_val('result/v1.0/')
    compute_val('result/v2.0/')
    compute_val('result/v2.5_rag/')
    compute_val('result/v2.6_brief/')
    compute_val('result/v2.7_new/')
    compute_val('result/v3.0_brief_prompt/')