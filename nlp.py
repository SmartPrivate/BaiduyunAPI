import logging
import json
import requests
import os
import sys

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)


class NLP(object):
    def __init__(self, print_result: bool = False, token_file: str = 'env/access_token.json'):
        self.__token_file = token_file
        self.__post_param = dict(access_token=self.__get_access_token())
        self.__print_result = print_result

    def __get_access_token(self):
        if not os.access(self.__token_file, os.R_OK):
            print('***未找到access_token文件，检查文件是否存在***')
            print('***第一次使用请运行token获取工具token_getter.py***')
            sys.exit(1)
        token_json_line = open(self.__token_file, 'r').readline()
        format_json = json.loads(token_json_line)
        return format_json['access_token']

    def __request_operator(self, post_data, post_url):
        post_json = json.dumps(post_data)
        try:
            response_text = requests.post(url=post_url, params=self.__post_param, data=post_json).text
            response_value: dict = json.loads(response_text)
            if self.__print_result:
                print(response_value)
            return response_value
        except requests.exceptions.ConnectionError:
            print('连接超时！请检查你的网络连接...')
            sys.exit(1)

    def word_sentiment(self, text: str):
        """
        情感分析接口
        :param text: str 待分析文本
        :return:
            分析结果dict，其中包含：
                sentiment: int 情感极性分类结果 0-消极 1-中性 2-积极
                confidence: float 分类置信度[0,1]
                positive_prob: float 积极概率[0,1]
                negative_prob: float 消极概率[0,1]
            错误结果dict，其中包含：
                error: str 错误信息
        """
        post_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify'
        r_dict = self.__request_operator(post_data=dict(text=text), post_url=post_url)
        if 'error_msg' in r_dict.keys():
            return dict(error=r_dict['error_msg'])
        return r_dict['items'][0]

    def lexical_analysis(self, text: str, stop_word_list: list = None):
        """
        词法分析借口
        :param text: str 待分析文本
        :param stop_word_list: list 停用词列表
        :return:
            分析结果dict list，其中每个dict包含：
                item: str 分词结果
                pos: str 词性
                ne: str 专有名词标识（如果ne有值则pos为空）
                basic_words: list 分词结果基础构成词
            错误结果dict，其中包含：
                error: str 错误信息
        """
        post_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer'
        r_data = self.__request_operator(post_data=dict(text=text), post_url=post_url)
        if 'error_msg' in r_data.keys():
            return dict(error=r_data['error_msg'])
        result_dict_list = []
        if stop_word_list:
            for item in r_data['items']:
                if item['item'] in stop_word_list:
                    continue
                result_dict_list.append(
                    dict(item=item['item'], pos=item['pos'], ne=item['ne'], basic_words=item['basic_words']))
        else:
            for item in r_data['items']:
                result_dict_list.append(
                    dict(item=item['item'], pos=item['pos'], ne=item['ne'], basic_words=item['basic_words']))
        return result_dict_list

    def word_emb_vec(self, word, convert_to_str: bool = False):
        """
        词向量表示接口
        :param convert_to_str: bool 是否将词向量转换为逗号分隔的字符串
        :param word: str 待表示的词
        :return:
            分析结果dict，其中包含：
                vector: str or list 词向量表示结果（1024维）
            错误结果dict，其中包含：
                error: str 错误信息
        """
        post_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v2/word_emb_vec'
        r_data = self.__request_operator(post_data=dict(word=word), post_url=post_url)
        if 'error_msg' in r_data.keys():
            return dict(error=r_data['error_msg'])
        if convert_to_str:
            vectors = list(map(lambda o: str(o), r_data['vec']))
            return dict(vector=','.join(vectors))
        return dict(vector=r_data['vec'])
