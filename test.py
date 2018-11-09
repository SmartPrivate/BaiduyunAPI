import logging
from nlp import NLP

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

nlp = NLP()
result=nlp.word_sentiment(text='今天是个好日子')
print(result)

result=nlp.lexical_analysis(text='我在武汉大学信息管理学院')
print(result)