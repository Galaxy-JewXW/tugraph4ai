import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import hashlib

from setting import *

# 用于存储成功访问的 URL
successful_urls = set()
# 用于存储每个页面内容的哈希值，去重使用
content_hashes = set()

# 计算页面内容的哈希值，避免重复
def get_content_hash(content):
    return hashlib.md5(content.encode('utf-8')).hexdigest()

# 定义递归函数，爬取每个页面
def crawl(url, base_url, depth):
    # # 如果已经访问过此URL，则跳过
    if url in successful_urls:
        return
    if depth > 100:
        return

    # 请求页面内容
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return

    # 计算页面内容的哈希值
    content_hash = get_content_hash(response.text)

    # 如果该页面内容的哈希值已经存在，说明内容重复，跳过该页面
    if content_hash in content_hashes:
        print(f"Duplicate content found at: {url}, skipping.")
        return

    # 保存该页面内容的哈希值
    content_hashes.add(content_hash)

    # 如果访问成功且内容不重复，保存这个 URL
    successful_urls.add(url)
    print(f"Successfully visited: {url}")

    # 解析页面
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找所有的链接，使用 'a' 标签
    for link in soup.find_all('a', href=True):
        # 获取链接的完整URL
        href = link.get('href')
        new_url = urljoin(url, href)  # 使用当前页面的 URL 作为基准

        # 检查是否为相同域名的链接
        if urlparse(new_url).netloc == urlparse(base_url).netloc:
            # 避免爬取无效的锚点链接和邮件链接
            if not new_url.endswith('#') and not new_url.startswith('mailto:'):
                # 去除 URL 中的片段（#及其后内容）
                new_url = new_url.split('#')[0]
                # 去除 URL 中的查询参数（?及其后内容），如果不需要可以保留
                new_url = new_url.split('?')[0]
                # 递归爬取新的页面
                crawl(new_url, base_url, depth + 1)

    # 爬取结束后，稍作休眠
    time.sleep(0.5)  # 避免爬虫过快爬取

# 进行爬取
crawl_urls = [
    "https://tugraph-db.readthedocs.io/zh-cn/latest/",
    "https://www.oceanbase.com/docs/tugraph-doc-cn",
]

doc_urls = [
    "https://www.modb.pro/db/656598",
    "https://www.modb.pro/db/1782579391289651200",
    "https://tugraph-db.readthedocs.io/zh-cn/v3.5.1/5.developer-manual/2.running/2.tugraph-running.html",
    "https://tugraph-db-lipanpan.readthedocs.io/zh-cn/latest/6.utility-tools/6.tugraph-cli.html",
    "https://tugraph-db-lipanpan.readthedocs.io/zh-cn/latest/8.query/3.vector_index.html",
    "https://www.modb.pro/db/483644",
    "https://tugraph-db.readthedocs.io/zh-cn/latest/6.utility-tools/1.data-import.html",
    "https://tugraph-db.readthedocs.io/zh-cn/latest/4.user-guide/1.tugraph-browser.html",
    "https://blog.csdn.net/gitblog_00098/article/details/142606629",
    "https://blog.csdn.net/gitblog_00098/article/details/142606629",
    "https://www.modb.pro/db/628435",
    "https://tugraph-db.readthedocs.io/zh-cn/v4.1.0/5.developer-manual/2.running/2.tugraph-running.html",
    "https://help.aliyun.com/zh/compute-nest/use-cases/tugraph-service-instance-deployment-documentation",
    "https://www.modb.pro/db/656572",
    "https://tugraph-db.readthedocs.io/zh-cn/latest/2.introduction/4.schema.html",
    "https://tugraph-db.readthedocs.io/zh-cn/latest/9.olap&procedure/",
]

def crawl_all_urls():
    with open(SUCCESS_URL_FILE, "r") as file:
        # 假设每一行是一个链接，strip()去除换行符
        successful_urls.update({line.strip() for line in file.readlines()})
    
    for start_url in crawl_urls:
        crawl(start_url, start_url, 0)
    
    # 将 doc_urls 添加到 successful_urls 集合中
    successful_urls.update(doc_urls)
    
    print(successful_urls)

    # 将成功访问的 URL 保存到文件
    with open(SUCCESS_URL_FILE, "w", encoding='utf-8') as f:
        for url in successful_urls:
            f.write(url + "\n")

    print(f"Successfully saved {len(successful_urls)} unique URLs to 'successful_urls.txt'.")

if __name__ == "__main__":
    crawl_all_urls()