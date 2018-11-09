# 百度云自然语言处理API的Python封装
详细功能描述请参考百度云  
[自然语言处理技术文档](https://cloud.baidu.com/doc/NLP/NLP-API.html)
## 可使用模块
### 1.词法分析接口
#### 主要功能
- 提供分词
- 词性标注
- 专名识别

能够识别出文本串中的基本词汇（分词），对这些词汇进行重组、标注组合后词汇的词性，并进一步识别出命名实体。

### 2.词向量表示接口
#### 主要功能
中文词向量的查询
### 3.情感分析接口
#### 主要功能
对包含主观观点信息的文本进行情感极性类别（积极、消极、中性）的判断，并给出相应的置信度
### 持续添加中...

## 使用方法
### 获取access token
1. 注册百度云API使用账号（百度账号通用）[传送门](https://login.bce.baidu.com/reg.html)
2. 根据需求创建应用
3. 获取应用`API Key`和`Secret Key`
4. 调用`token_getter.py`模块获取`access token`
```bash
python token_getter.py -a 12345  -s 12345 access_token.json
```
### 接口调用方法示例
```python
from nlp import NLP

# 实例化NLP类
nlp = NLP()

# 情感分析接口
result=nlp.word_sentiment(text='今天是个好日子')
print(result)
```
