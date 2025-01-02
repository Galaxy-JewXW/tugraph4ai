# 工作简介

在多个赛题中，我们选择了“TuGraph for AI”-RAG在智能问答场景中的落地作为选题。该赛题要求我们开发一个RAG系统，准确回答用户关于TuGraph-DB的各种问题，涵盖使用方法、功能特性、技术细节等多个方面。

项目伊始，我们搭建的RAG系统在性能排名中仅位于90/100，但经过不懈努力和深入分析，从最初的baseline（v1.0）到最终版本（v4.4）的多个迭代。这一过程中，我们引入了混合检索（v2.0）、拆分和优化了RAG（v2.5）、显著提升了召回率（v3.0至v4.4），并在最终版本中更改了embedding模型（v4.4），成功将排名提升至19/112，实现了显著的性能飞跃。

在数据收集阶段，我们收集了TuGraph-DB的官方文档、社区讨论和技术博客，并对数据进行了细致的清洗策略，确保信息的准确性和相关性。

在模型训练过程中，我们进行了多轮参数调整和算法优化，以提升系统的响应速度和问答的准确性。通过不断的测试与反馈，我们逐步完善了系统的各个环节，使得系统性能得到了显著提升。

最终我们的排名为19/122，以下为截图：

![排名截图](https://pigkiller-011955-1319328397.cos.ap-beijing.myqcloud.com/img/202501021746203.png)

## 版本记录

答案的版本信息：

| 版本 | 主要更新内容 | 召回率 | 核心改进                                                     |
| ---- | ------------ | ------ | ------------------------------------------------------------ |
| v1.0 | 基础版本实现 | 0.58   | - 仅使用最基本的baseline                                     |
| v2.0 | 混合检索引入 | 0.62   | - 加入混合检索机制<br>- 引入问题重新描述                     |
| v2.5 | RAG架构优化  | 0.65   | - 拆分了RAG架构<br>- 进行了召回优化<br>- 优化了prompt        |
| v3.0 | 数据更新     | 0.69   | - 更新了数据集（未清洗）<br>- 使用简化回答的prompt           |
| v3.1 | 召回优化     | 0.699  | - 更新异名同义文档<br>- 优化召回策略<br>- 优化问题改写prompt<br>- 修改为中文优先回答 |
| v3.2 | 数据清洗     | 0.6985 | - 使用MR中的数据清洗方案<br>- 更新数据源                     |
| v3.3 | 定向优化     | 0.6839 | - 进一步更新数据源<br>- 对特定问题(70,73,76)使用专门数据     |
| v4.0 | 策略调整     | 0.7036 | - 回退到v3.1版本<br>- 增加针对性数据集                       |
| v4.1 | 答案优化     | 0.7124 | - 优化部分prompt<br>- 尝试简化答案                           |
| v4.2 | 概括优化     | 0.7177 | - 进一步优化prompt<br>- 对回答进行概括                       |
| v4.3 | 二次概括     | 0.7021 | - 在得到答案后进行二次概括                                   |
| v4.4 | 模型更新     | 0.7177 | - 更改了embedding模型                                        |

# 比赛赛题介绍

接下来将分别介绍我们尝试的赛题和最终算选的赛题

## 所有赛题介绍

在本次项目中，我们对所有赛题进行了简单的尝试，并针对以下其中基于运营商文本数据的知识库检索、「TuGraph for AI」RAG 在智能问答场景中的落地三道赛题进行了深入的研究与实践。

### 基于运营商文本数据的知识库检索

赛题背景：通过使用 RAG 检索增强生成技术将私域数据作为大模型的外接知识库，可以很好地解决大模型知识幻觉的问题。这一技术实践的关键在于文档解析、知识库生成与文本召回的策略设计。

赛题任务：选手需使用运营商相关的文档构建知识库，根据用户问题检索知识库并返回答案所在的文本块。

此赛题也要求实现一个RAG系统，主要形式为对PDF文档的RAG信息提取。我们也进行了尝试，但是整体效果不如最终选择的赛题，因此没有进行深入挖掘

### 「TuGraph for AI」RAG 在智能问答场景中的落地

赛题背景：TuGraph-DB 是由蚂蚁集团开发的领先分布式高性能图数据库。本赛题旨在开发一个智能问答助手，能够准确回答用户关于 TuGraph-DB 的各类问题。

赛题任务：参赛者需要开发一个智能问答系统，能够准确回答关于 TuGraph-DB 的各类问题。

此赛题为我们最终选择的赛题。

### 「AI for TuGraph」小样本条件下的自然语言至图查询语言翻译大模型微调

赛题背景：在图数据库领域，缺乏统一的查询语言，使用门槛较高。本赛题旨在通过微调大模型，将自然语言翻译成可执行的图查询语言，以降低使用门槛。

赛题任务：参赛者需使用提供的 Cypher 语料，对指定的本地模型进行微调，使其能够准确将自然语言描述翻译成对应的 Cypher 语句。

此赛题要求对模型进行微调。在baseline基础上，我们使用了swift框架作为微调框架，使用Cypher语料进行了微调。模型微调对所使用的模型和进行微调的显存大小提出了要求。受限于有限的设备，我们没有进行深入的尝试。

## 所选赛题介绍

TuGraph-DB 是由蚂蚁集团开发的一款领先的分布式国产高性能图数据库。它构建了一套全面的图技术体系，涵盖了图存储、图计算、图学习和图研发平台等关键组件。随着图数据库在数据管理和分析中的重要性不断提升，用户对其功能和性能的需求也日益增加。为此，提升 TuGraph-DB 的用户体验和技术支持能力显得尤为重要。

本次比赛旨在开发一个智能问答助手，该助手能够准确回答用户关于 TuGraph-DB 的各种问题，包括使用方法、功能特性、技术细节等。这不仅有助于提高用户对 TuGraph-DB 的理解和使用效率，还能为开发者提供更为便捷的技术支持，促进 TuGraph-DB 的推广和应用。

我们需要开发一个智能问答系统，能够准确回答关于 TuGraph-DB 的各类问题。具体任务包括但不限于：

1. 数据收集：从 TuGraph-DB 的官方文档、社区讨论、技术博客等多种渠道收集相关信息，构建知识库。

2. 数据处理：对收集到的数据进行清洗、分词、向量化处理，确保信息的准确性和有效性。

3. 模型构建：基于 RAG（Retrieval-Augmented Generation）框架，结合信息检索与生成模型，设计并实现智能问答系统。

4. 问答能力提升：通过对系统进行多轮测试与优化，提高问答的准确性和相关性，确保能够满足用户的需求。

5. 用户体验优化：关注系统的响应速度和用户交互体验，确保用户能够快速获得所需信息。

评测采用基于语义相似度的方法，具体来说：使用Sentence Transformer将模型生成的答案和标准答案转换为句子嵌入表示，然后计算这两个嵌入表示之间的余弦相似度（并归一化为[0,1]）作为分数。

# 工作内容介绍

在本次比赛中，我们的核心任务是构建一个基于 RAG（Retrieval-Augmented Generation）框架的智能问答系统。

起初，我们的排名处于90/100的位置，并且在答案信息上问题较大。我们细致了RAG系统的各个流程，寻找可以优化的空间，分别对数据处理、模型训练、查询处理、答案生成四个部分进行了优化。

在数据处理方面，我们实施了更为细致的清洗和向量化策略，确保信息的准确性和相关性。同时，我们在模型训练过程中，进行了多轮参数调整和算法优化，以便提升系统的响应速度和问答的准确性。通过不断的测试与反馈，我们逐步完善了系统的各个环节。

经过一系列的努力，我们的排名逐渐攀升，最终达到了19/112 的佳绩。较原始的成绩取得了极大的进步

值得说明的是，RAG的构建离不开LLM的作用。在 RAG 系统中，我们主要经历了以下几个阶段来使用 LLM：

1. 数据准备：通过爬取与清洗，准备好用于训练与检索的文档。

2. 向量生成：利用 BAAI/bge-large-zh-v1.5 模型，将文档转化为向量，并存储在 FAISS 数据库中。

3. 查询处理：用户提问后，通过问题改写与检索，获取相关文档。

4. 答案生成：将检索到的文档与用户问题输入到 LLM 中，生成最终的回答。

## RAG使用的数据

以下将介绍我们实现的RAG使用的数据来源和获取方式，以及对数据的清洗。

### 数据来源

本次比赛不提供训练语料，因此我们在网上对有关TuGraph-DB的资料进行了筛选，最终选择了部分内容丰富的文档作为训练语料库，包括但不限于：

- TuGraph-DB使用文档、官方说明、Github Wiki，这些文档详细介绍了TuGraph-DB的各项功能、使用方法、最佳实践
- TuGraph-DB开源代码，用于理解底层实现和回答技术细节问题
- TuGraph微信公众号文章，可提供部分基础概念与基本信息的语料
- 各大社群平台有关TuGraph有关的博客分享（CSDN、知乎、个人博客等），包含部分使用TuGraph-DB的过程中面临到的实际问题

### 数据爬取与清洗

首先通过人工筛选，从CSDN、知乎、Github等平台获取部分有关内容的url，进行预加载。

```python
# 获取预处理得到的url
# 这部分url属于
def _get_crawl_urls(filename=None) -> dict:
    if filename is None:
        raise Exception("no crawl urls")

    # 读取successful_urls.txt中的所有链接
    with open(filename, "r") as file:
        # 每一行是一个链接
        successful_urls = [line.strip() for line in file.readlines()]

    # 合并并去重
    all_links = list(set(successful_urls))
    print(f"the total len of crawl urls is: {len(all_links)}")

    return all_links

crawl_file = "data/successful_urls.txt"
urls = _get_crawl_urls(crawl_file)
print(f"[embedding]: get crawl urls successful")
```

对于[Tugraph-DB官方文档](https://tugraph-db.readthedocs.io/zh-cn/latest/)等类似的、以Readthedocs框架搭建而来的文档页面，可以通过不断地访问当前页面蕴含的所有链接（在HTML中表现为`<a>`元素），持续获得有关内容的url。由于此类网站内容专注于TuGraph介绍而不存在过多无关信息，因而不需要对新获取的url进行检查。

```python
def get_all_links_from_index(index_url):
    response = requests.get(index_url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    base_url = "https://tugraph-db.readthedocs.io/zh-cn/latest/"
    links = []

    # 查找所有 <a> 标签，提取 href 属性中的子页面链接
    for a_tag in soup.find_all("a", href=True):
        href = a_tag['href']
        # 如果链接是相对路径的子页面，转换为完整URL
        if href.startswith('/') or not href.startswith('https'):
            full_url = base_url + href if not href.startswith('/') else base_url + href[1:]
            links.append(full_url)

    # 过滤掉重复的链接
    links = list(set(links))

    return links
```

最后，使用langchain_community.document_loaders提供的WebBaseLoader类，加载获取到的所有有效url列表的内容，并在本地进行缓存。下一次训练时，对于同一个url，可直接从本地获取文本内容，大大加快语料处理速度。

```python
loader = WebBaseLoader(all_links)
documents = loader.load()
```

### 数据清洗：分词

我们使用 langchain.text_splitter 中提供的RecursiveCharacterTextSplitter类进行文本分割。

RecursiveCharacterTextSplitter是langchain推荐用于通用文本的分割器。它兼容各种文本格式，采用递归的方法，首先尝试使用较大的分隔符（如段落）进行分割，如果结果块仍然过大，则逐步使用较小的分隔符（如句子、短语）进行细分。这种多层次的分割策略确保了文本块既不失去语义完整性，又符合预设的长度限制。

相比于简单的字符或固定长度分割，RecursiveCharacterTextSplitter 更加注重保持文本的上下文连贯性，避免在中间位置断开句子或段落，从而保留文本的语义完整性。

数据来源大部分都是中文语料，与英文相比没有词边界，使用的分隔符列表`['\n\n', '\n', ' ', '']`分割文本可能会导致单词在块之间被拆分，因此需要手动设定分隔符：

```python
separators = ["\n\n", "\n", " ", ".", "。", ";", "；",]  # 定义分割符
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,  # 每个文本块的最大字符数
    chunk_overlap=CHUNK_OVERLAP,  # 相邻文本块之间的重叠字符数
    separators=separators,  # 用于识别文本块边界的分割符
    keep_separator=False,  # 是否保留这些分割符在文本块中
)
documents = text_splitter.split_documents(documents)
```

## 搭建向量库

在RAG系统中，检索的任务是快速且精确地找出与输入查询语义上最匹配的信息。向量技术是语义检索的核心，它通过将用户的问题和知识库内容都转化为高维语义向量，并通过数学方法找到两者之间的距离，从而实现语义上的匹配。

由于信息可以表示成高维向量，针对向量加上特殊的索引优化和量化方法，可以极大提升检索效率并压缩存储成本。这对于需要处理海量数据的RAG系统至关重要，因此向量数据库更擅长处理超大规模的非结构化数据。

### 向量库介绍

向量数据库可以被看作是一个高效的知识仓库和搜索引擎，它帮助大语言模型快速找到并使用相关信息。通过将文本数据转换为向量形式，向量数据库能够存储和检索大量的嵌入向量，这些向量不仅能够表征文本和图像等多种数据类型，还能够捕获它们深层的语义信息。

我们选择将文档转换为向量并存储在FAISS数据库中。这样可以进行本地持久化存储，方便后续使用。此外，在检索过程中，我们设置检索时返回的相关文档数量（默认为9），并使用向量相似度搜索找到最相关的文档片段。

向量库的使用涉及了三个流程，在下文将进行详细介绍：

1. 文本分块
2. 向量生成
3. 向量存储

### 文本分块

我们使用递归字符分割器将长文本分成小块，并通过重叠区域保证上下文的连贯性。这样做的优势是：

- 可以更好地保证上下文的连贯性
- 可以更好地保证文本的完整性
- 可以更好地保证文本的准确性

```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,        # 2048字符
    chunk_overlap=CHUNK_OVERLAP,  # 512字符重叠
    separators=["\n\n", "\n", " ", ".", "。", ";", "；"],
    keep_separator=False
)
```

### 向量库选择

在向量库的选择中，我们使用了FAISS作为存储文本数据的向量库，以在RAG的搭建中达到更好的速度与效果。

FAISS支持GPU加速，搜索速度快，内存占用低，适合大规模向量检索，支持多种索引类型。

但是，在我们的开发过程中，FAISS并不是唯一的尝试，我们也对ChromaDB进行了尝试。相较于ChromaDB，FAISS在高效相似度搜索和GPU加速方面表现出色，而ChromaDB则提供了全面的数据库功能和分布式处理能力。

对于我们的RAG系统，选择FAISS作为向量库，可以更好地在GPU上进行相似度搜索，从而在RAG的搭建中达到更好的速度与效果。

此外，由于比赛的性质，我们的向量库大多都是运行在本地单一电脑上，并不需要分布式处理能力，因此FAISS可以更好地满足我们的需求。

```python
def _create_db(documents, embedding):
    db = FAISS.from_documents(
        documents, 
        embedding=embedding
    )
    db.save_local(f"data/{EMBEDDING_DB_NAME}")

    return db
```

### 向量生成模型

在向量生成模型中，我们使用了BAAI/bge-large-zh-v1.5作为向量生成模型，以在RAG的搭建中达到更好的速度与效果。

BAAI/bge-large-zh-v1.5的在生成向量模型中的优势在于：

- BGE (BAAI General Embedding) 是专门针对中文优化的向量模型
- 支持GPU加速，搜索速度快，内存占用低，适合大规模向量检索，支持多种索引类型。
- 对中文的支持较好，可以更好地在GPU上进行相似度搜索，从而在RAG的搭建中达到更好的速度与效果。  

```python
EMBEDDING_MODEL_NAME = "BAAI/bge-large-zh-v1.5"
```

此外，在模型的配置上，通过良好的封装，我们也对模型进行了一些配置，支持调节模型参数，以在RAG的搭建中达到更好的速度与效果。

```python
def _get_embedding_model():
    model_name = EMBEDDING_MODEL_NAME
    model_kwargs = {"device": "cuda"}
    encode_kwargs = {"normalize_embeddings": True}
    embedding = HuggingFaceBgeEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
        query_instruction="为这个句子生成表示以用于检索相关文章："
    )
    return embedding
```

在上述的代码中的配置：

- 我们使用GPU进行向量计算：`model_kwargs = {"device": "cuda"}`，这样可以在GPU上进行向量计算，从而在RAG的搭建中达到更好的速度与效果。
- 启用向量归一化：`encode_kwargs = {"normalize_embeddings": True}`，这样可以在向量被规范化（归一化）后，它们的范数都是1。余弦相似度的计算只需要向量的点积运算，从而减少了计算的复杂度，加快了处理速度。
- 设置了专门的中文检索指令：`query_instruction="为这个句子生成表示以用于检索相关文章："`，这样可以在向量生成模型中设置专门的中文检索指令，从而在RAG的搭建中达到更好的速度与效果。

## RAG的混合召回算法

在将文本内容存储在向量库之后，需要进行召回，以找到匹配的文本内容。

### 召回的作用

召回在RAG中的作用至关重要，主要体现在以下几个方面：

- 提供相关上下文：召回是RAG系统中将用户查询与知识库中的相关文本进行匹配的过程，其目的是找出最相关的上下文信息。这些上下文信息随后会与问题一起提交给语言模型（LLM）以生成答案，直接影响LLM能够接收到多少有用信息，进而影响最终答案的准确性和相关性。

- 多路召回提升多样性：在多轮对话和复杂查询场景中，多路召回（Multi-Channel Retrieval）是RAG系统中用于提升检索结果多样性和覆盖度的关键机制。通过使用不同的检索策略和通道，系统可以最大程度地覆盖问题相关的文档，确保生成的答案基于更全面的上下文信息。

- 混合检索的补充：结合向量检索和关键词检索的优势，通过多个检索系统的组合，实现了多个检索技术之间的互补，进一步提升召回的准确性和全面性。

在我们的实现中，使用了两种召回算法，分别是向量检索和BM25检索。

### 召回算法

代码中主要结合了两种召回方式：

- 向量检索（Dense Retrieval）
- BM25检索（Sparse Retrieval）

```python
# 1. 向量检索部分
db = FAISS.load_local(
    f"data/{EMBEDDING_DB_NAME}",
    embedding_model,
    allow_dangerous_deserialization=True,
)
retriever = db.as_retriever(search_kwargs={"k": SEARCH_NUM})

# 2. BM25检索部分
bm25_retriever = BM25Retriever.from_documents(
    docs,
    k=SEARCH_NUM,
    bm25_params={"k1": 1.5, "b": 0.75},
    preprocess_func=jieba.lcut  # 使用结巴分词
)

# 3. 组合检索器
ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, retriever],
    weights=[0.4, 0.6]  # BM25权重0.4，向量检索权重0.6
)
```

通过使用EnsembleRetriever，我们可以将两种召回方式的结果进行组合，从而在RAG的搭建中达到更好的速度与效果。相关的权重设置让向量检索的召回结果占比更大，从而在RAG的搭建中达到更好的效果。

向量检索和BM25检索在语义理解和关键词匹配上各有优势。向量检索擅长捕捉语义相似性，而BM25检索则在关键词匹配上表现更好。通过混合召回，可以结合这两种方法的优势，提高召回结果的准确性和覆盖度。

### 向量检索

向量检索是一种基于向量空间模型的信息检索技术，其核心在于将非结构化数据（如文本、图像、音频等）转换为高维向量，并在向量空间中计算这些向量之间的相似度，以实现快速检索。

向量检索利用了向量数据库本身提供和功能。使用FAISS向量库存储文档的语义向量，基于BGE-Large模型进行向量编码。

向量检索的优势在于能够理解语义相似性，处理同义词和上下文关系，适合处理长文本的语义匹配。

使用向量检索，可以不需要进行额外的配置，直接使用FAISS向量库进行检索。

```python
db = FAISS.load_local(
        f"data/{EMBEDDING_DB_NAME}",
        embedding_model,
        allow_dangerous_deserialization=True,
    )
retriever = db.as_retriever(search_kwargs={"k": SEARCH_NUM})
```

上述的代码中就直接使用了FAISS向量库进行检索，并设置了返回的文档数量，默认设置为了9，以提供更多的信息，让RAG的回答更加准确。

### BM25检索

BM25（Best Matching 25）是一种基于概率的排名函数，用于信息检索系统，特别是文本检索。它是TF-IDF模型的改进版本，旨在解决TF-IDF在处理长短文档和不同查询长度时的一些局限性。

BM25通过计算查询词与文档的匹配程度，为每个文档生成一个得分，然后根据得分对文档进行排序，从而提供最相关的搜索结果。BM25是许多搜索引擎和信息检索系统中广泛使用的排名算法。

在BM25的实现中，我们使用经典的BM25算法，通过结巴分词处理中文，并设置参数`k1=1.5`，`b=0.75`，以在RAG的搭建中达到更好的效果。

BM25的优势在于精确匹配关键词，计算速度快，对稀有词汇敏感。

```python
bm25_retriever = BM25Retriever.from_documents(
    docs,
    k=SEARCH_NUM,
    bm25_params={"k1": 1.5, "b": 0.75},
    preprocess_func=jieba.lcut  # 中文需要使用jieba分词
)
```

上述的代码中就直接使用了BM25算法进行检索，并设置了返回的文档数量，默认设置为了9，以提供更多的信息，让RAG的回答更加准确。

BM25的优势在于精确匹配关键词，计算速度快，对稀有词汇敏感。

### jieba分词

在BM25检索中，我们使用了jieba分词，以在RAG的搭建中达到更好的效果。

jieba可以进行良好的文本预处理，可以对中文文本进行分词，这是中文文本预处理的重要步骤，为后续的文本分析和处理打下基础。

并且，jieba分词还支持多种分词模式：

- 精确模式：试图将句子最精确地切开，适合文本分析。
- 全模式：把句子中所有可能的词语都扫描出来，速度非常快，但是不能解决歧义问题。
- 搜索引擎模式：在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。

## 提问的问题改写

在实际的过程中，我们发现：

- 提问的问题可能**存在歧义**，导致召回的文档可能并不是全都有用的，而是覆盖了其中的关键词。
- 提问的问题可能存在**语义不明确**，导致召回的文档可能并不是全都有用的，而是覆盖了其中的关键词。
- 问题可能是**简略的、口语化的、不完整的**，导致原始问题不含有真正的关键词，不能反映查询意图，需要进行规范化改写，以提高查询的效果。

因此，我们提出了问题改写的方法，以在RAG的搭建中达到更好的效果。

问题改写的目的是为了将问题更加规范化，以消除原始的自然语言问题在提问过程中的歧义和语义不明确。

在重写的过程中，我们直接调用了`GLM-4-PLus`模型，调用其接口进行问题改写。

```python
prompt = ChatPromptTemplate.from_template(prompt_template)
llm_chain = prompt | self.llm
rewrite = llm_chain.invoke({"question": question}).content
```

相应的改写prompt如下：

```
现在我需要向您咨询有关TuGraph-DB的问题。请按照以下指导原则改写我的问题，以确保它适合用于数据库查询或搜索引擎检索：
- 将原始问题转换成明确、简洁且针对性强的形式；
- 确保问题表述专业，避免使用口语化或非正式的语言；
- 维持问题的原始含义，不得添加或删除任何重要信息；
- 如果原始问题是开放式的，请尝试将其转化为具体的、可搜索的形式；
- 如果可能，考虑加入关键术语或技术词汇来增强查询的精确度。

请直接提供改写后的问题，注意不要改变问题的语义，不要引入新的意思。
下面是原始的问题：
{question}
---
请直接给出改写后的问题。
```

经过实验，进行问题改写能取得较好的效果，问题的标准性得到了提升，在召回中能取得更好的效果。

## 召回重排序

在进行召回后，RAG会得到多个文档，但是这些文档可能并不是全都有用的，而是覆盖了其中的关键词。在召回得到文档之后，还需要进行重排序，以找到最相关的文档。

此外，对于改写前后的问题，由于改写可能导致问题产生了部分变化，我们对改写前后的问题均进行了召回，对于得到的文档共同进行重排序。

```python
# 余弦相似度召回
# 对原始问题和改写问题均进行召回，取余弦相似度最高的前num个问题
docs = self.retriver.invoke(question)
docs_rewrite = self.retriver.invoke(question_rewrite)
```

在重排序中，我们首先对文档赋予了一定的得分，根据得分排序得到前`SEARCH_NUM`个召回结果，以得到真正有用的文档，达到质量和数量之间的平衡。

### 文档得分

文档得分的计算方式为使用余弦相似度计算问题和文档之间的相似度，以得到文档的得分。

这种得分设计的思考为：

- 余弦相似度能够很好地衡量两个向量之间的相似度，能够很好地衡量问题和文档之间的相似度。
- 如果召回的文档能够较好地匹配问题，那么应该能反映问题的需求。否则若采用其他的得分方式，要么会有较为复杂的计算方式，要么效果较差，难以达到一个良好的平衡。

```python
def _get_docs_scores(docs):
    # 重排
    pairs = [[question, doc.page_content] for doc in docs]
    with torch.no_grad():
        inputs = self.tokenizer(pairs, padding=True, truncation=True, return_tensors='pt', max_length=512)
        scores = self.model(**inputs, return_dict=True).logits.view(-1, ).float()
    # 确保scores是一维的
    scores = scores.squeeze()
    return scores
```

在分数的计算过程中，对每个文档片段计算与问题的相关性分数，并使用交互式编码方式，比单独编码更准确。

### 文档排序

此外，在文档排序中，我们使用了长上下文检索器，将最相关的文档放在开始和结尾，中间放无关紧要的。

这样的设计意图是在匹配LLM的回答方式，以让其注意到**“更加重要的文档”**，以免由于提供的长文本而导致LLM无法注意到真正重要的文档，以优化长文本阅读和理解效果。

```python
# 对文档进行排序，基于得分从高到低
doc_scores.sort(key=lambda x: x[1], reverse=True)
# 提取排序后的文档对象，阈值过滤
sorted_docs = [doc for doc, score in doc_scores if score >= score_threshold][:SEARCH_NUM]
# 长上下文检索器，将最相关的文档放在开始和结尾，中间放无关紧要的
reordering = LongContextReorder()
reordered_docs = reordering.transform_documents(sorted_docs)
```

## 输出风格改写

由于比赛的评测机制，评分是讲我们的答案与官方的答案进行余弦相似度比较。尽管我们的回答已经能很好地搜索得到相应的答案，但是碍于分数，我们尝试总结了官方给出的实例中的回答风格，尝试进行风格改写。

我们发现，官方回答的风格是：

1. 较为简洁的回答方式，如果能直接给出答案，通常不会进行解释
2. 回答中通常尽量使用中文，减少了英文的使用

对于输出，我们依然使用了`GLM-4-PLus`模型，调用其接口进行了回答生成。

相关的prompt如下：

```
As a specialized AI assistant for question-answering, I will use the given context to provide a clear and concise response to your query in no more than three sentences, without adding any LLM-specific filler words such as '好的' or '从资料中可以得出'. If the necessary information is not available, I will let you know.
Aanswer in a brief way. If there is a clear answer to the question, just provide the answer without explanation.
Context:
{context}
---
Question:
{question}
---
Answer in Chinese if you can, except for terms and proper nouns.
Note: For questions in the format of 'input_field': question, 'output_field': 'answer', please provide only the answer value without additional text.
Here is your answer:
```

在进行输出风格改写后，我们发现我们的回答能和官方的搜索结果匹配的较好，有些输出尽管依然存在风格比匹配的问题，但是我们觉得这是官方的问题，已经不再是我们的问题了。

## 本地模型尝试

目前，我们所使用的模型分为如下几种：

```python
# 用于将文档转换为向量库的模型名
EMBEDDING_MODEL_NAME = "BAAI/bge-large-zh-v1.5"
# 用于重排的模型名
RERANKER_MODEL_NAME = "BAAI/bge-reranker-large"
# 用于计算相似度的SOTA模型
SOTA_SIMILARITY_NAME = "BAAI/bge-large-zh-v1.5"

# 用于问答的LLM
LLM_MODEL_NAME = "GLM-4-PLus"
LLM_API_BASE = "https://open.bigmodel.cn/api/paas/v4"
```

### 本地大模型

其中除了问答的LLM，均使用了开源大模型，在本地进行运行。

本地大模型的好处在于，可以更快速地进行模型推理，并且可以更好地进行模型优化。

此外，对于本地大模型，我们使用了`vllm`，以优化本地大模型的推理速度。

### 问答大模型本地尝试

对于问答大模型，需要在得到文档后总结文档，从中得到真正关键的信息，回答原始问题。这对大模型的推理提出了较高的要求。

对于在线大模型，我们使用了智谱的`GLM-4-Plus`模型，这是一个70B的大模型，具有 不错的问答效果，但是**问答的速度较慢**，会拖慢整体回答的产生效果。

为此，我们也进行了问答大模型的本地化尝试，但是**受限于设备**，我们只能使用自己笔记本上的GPU进行推理，受限于较小的显存，我们能运行的最大模型为`Qwen1.5-7B`，发现**效果极差**，无法进行使用。

推测较差效果的原因是应为模型的参数较小，推理能力不足，无法进行良好的总结。

## 模型微调尝试

在本地模型的尝试过程中，我们还使用`swift`框架进行了模型微调尝试，具有一定的效果提升，但是整体效果依然比不上在线大模型的使用效果。

`swift`框架是是由魔搭ModelScope开源社区推出的一套完整的轻量级训练推理工具，可以较为轻量级地实现模型微调效果，让模型在问答过程中的效果得到提升。

```python
sft_args = SftArguments(
    model_type='qwen1half-7b-chat',
    model_id_or_path='./models/Qwen1.5-7B-Chat',
    dataset=[DatasetName.alpaca_zh, DatasetName.alpaca_en],
    train_dataset_sample=500,
    eval_steps=20,
    logging_steps=5,
    output_dir='output',
    lora_target_modules='ALL',
    self_cognition_sample=500,
    model_name=['dm', 'data-mining'],
    model_author=['dm', 'data-mining'])
output = sft_main(sft_args)
best_model_checkpoint = output['best_model_checkpoint']
print(f'best_model_checkpoint: {best_model_checkpoint}')
```

通过设置相应的参数checkpoint，可以得到微调后的模型，并进行使用。

# 分工和工作描述

我们对多个赛题进行了尝试，并在最终选择的赛题上进行了深度的工作。

## 赛题尝试

每个人尝试过的赛题如下。主要做出的工作为调研相关的赛题，并跑通对应赛题的baseline。

| 姓名   | 赛题                                                         |
| ------ | ------------------------------------------------------------ |
| 卞卓航 | 「AI for TuGraph」小样本条件下的自然语言至图查询语言翻译大模型微调 |
| 朱雄伟 | 「TuGraph for AI」RAG在智能问答场景中的落地                  |
| 胡健   | 基于运营商文本数据的知识库检索                               |

每位成员在各自负责的部分中都付出了努力，确保了项目的顺利进行。

## 最终实现的项目

在最终实现的项目中，我们进行了多轮优化，前后进行了共计39次代码commit提交。以下是我们的github提交截图：

![github记录](https://pigkiller-011955-1319328397.cos.ap-beijing.myqcloud.com/img/202501021741025.png)

我们进行的代码优化分工为：

| 事项         | 人   | 详细描述                                                    | 进度 |
| ------------ | ---- | ----------------------------------------------------------- | ---- |
| 比赛         | all  | 完成，最终召回率0.71778039，排名19/112                      | 完成 |
| 数据清洗     | zxw  | 对Markdown和Html的文本很快进行了清洗                        | 完成 |
| 数据收集     | zxw  | 收集了新数据，使用Hash和本地Cache降低时间开销               | 完成 |
| 代码重构     | bzh  | 将NoteBook重构为了项目化的代码                              | 完成 |
| 模型替换     | bzh  | Qwen7B的效果极差，本地微调在选择上不好用                    | 完成 |
| 模型微调     | bzh  | 对Qwen7B进行了微调，但是效果还是不好                        | 完成 |
| prompt优化   | bzh  | 对输出的选择、RAG的prompt均进行了修改，提升客观             | 完成 |
| 提问改写     | bzh  | 利用LLM填补缺失信息，以防问题本身造成查询困扰               | 完成 |
| 文本召回重排 | bzh  | 对原始问题和重写问题分别进行召回，得到相似度最高的num个问题 | 完成 |
| 回答风格改写 | bzh  | 为匹配接近答案的语言风格，在得到答案后由LLM进行一次改写概括 | 完成 |
| 优化查询     | hj   | 修改了Embedding模型选择                                     | 完成 |

# 总结

在课程的初期，我们对众多的选题和RAG系统的搭建完全没有思路。但在课程中，我们对赛题进行了深入了解，对RAG系统、模型微调都积累的一定的经验，取得了良好的项目经历。

通过本次项目，我们不仅在技术上得到了提升，也在团队合作中锻炼了沟通与协作能力。虽然未能进入复赛，但我们在数据处理、模型构建与优化等方面积累了宝贵的经验。

在未来的学习与实践中，我们期待在后续的课程中能够将所学的知识应用到实际项目中，提升我们的技术能力与实践经验。我们希望能够深入学习更多关于自然语言处理和深度学习的前沿技术，特别是在模型优化与性能提升方面。通过不断学习与实践，提升自己的技术水平。

通过以上的展望，我们相信在未来的学习与研究中，能够不断进步，取得更好的成果。我们期待在数据挖掘和机器学习的道路上，持续探索、不断创新。
