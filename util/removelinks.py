import re

def remove_all_links(text):
    # 删除 Markdown 链接，包括链接的文字内容
    text = re.sub(r'\[[^\]]+\]\([^)]+\)', '', text)
    # 删除 HTML 链接，包括链接的文字内容
    text = re.sub(r'<a\s+href="[^"]*">.*?</a>', '', text)
    # 删除纯 URL
    text = re.sub(r'http[s]?://\S+', '', text)
    return text

def process_single_file(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # 删除所有链接
    cleaned_text = remove_all_links(text)

    # 将处理后的文本写回文件（覆盖原文件）
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)
    print(f"已处理文件: {file_path}")

# 指定要处理的文件路径
file_path = 'data/docs/9.olap&procedure/1.procedure/3.cpp.md'
process_single_file(file_path)
