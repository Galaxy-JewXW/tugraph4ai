## 项目概述

执行逻辑：在此目录执行`python code/run.py`或其他python文件

## 活动记录

活动记录：

| 事项         | 人   | 详细描述                                                    | 进度 |
| ------------ | ---- | ----------------------------------------------------------- | ---- |
| zxw          |      |                                                             |      |
| 数据清洗     | zxw  | 对Markdown和Html的文本很快进行了清洗                        | 完成 |
| 数据收集     | zxw  | 收集了新数据，使用HASH和本地Cache降低时间开销               | 完成 |
| bzh          |      |                                                             |      |
| 模型替换     | bzh  | Qwen7B的效果极差，本地微调在选择上不好用                    | 完成 |
| prompt优化   | bzh  | 对输出的选择、RAG的prompt均进行了修改，提升客观             | 完成 |
| 提问改写     | bzh  | 利用LLM填补缺失信息，以防问题本身造成查询困扰               | 完成 |
| 文本召回重排 | bzh  | 对原始问题和重写问题分别进行召回，得到相似度最高的num个问题 | 完成 |
| hj           |      |                                                             |      |
| 优化查询     | hj   |                                                             |      |
| 召回重拍     | hj   |                                                             |      |

还可以做的：

- LLM无法理解具体含义，当无法理解时，多轮询问，A的B：先问A再问B
- 输出格式更加匹配答案形式

## 版本记录

答案的版本信息：

- v1.0：仅使用最基本的baseline
- v2.0：加入混合检索，引入了问题重新描述
- v2.5：拆分了RAG，进行了召回，优化了prompt
- v3.0：召回率来到0.69
  - 更新了数据集，但是还是没有清洗
  - 使用简化回答的prompt
- v3.1：召回率0.699
  - 更新了异名同义文档
  - 对召回进行了优化，对原始问题和改写问题同时进行查找，取召回率最高的前num个结果
  - 优化了问题改写的prompt
  - 修改prompt为尽量使用中文回答问题
- v3.2：召回率0.6985
  - 更新了数据源，使用了MR中的数据清洗
- v3.3：召回率0.6839
  - 进一步更新数据源，使用了MR中的数据清洗
  - 对一些问题使用了专门的数据（70、73、76）
- v4.0：召回率0.7036
  - 回退到v3.1
  - 增加了针对性数据集
- v4.1：召回率0.7124
  - 优化部分prompt，尝试让答案更简洁
- v4.2：召回率0.7177
  - 进一步优化prompt，对回答进行概括
- v4.3：召回率0.7021
  - 在得到答案后进行一次概括
- v4.4：
  - 更改了embedding模型
