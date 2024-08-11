"""
摘要器、萃取器、压缩器、理解器。理解一个 url。
"""

# coding = utf8

import requests
from bs4 import BeautifulSoup

from daily.abstrct.abstrctor_result import DocAbstractResult
from daily.api.openai.chat_completion_api import openai_chat_completion_api

class DocAbstractor(object):
    def __init__(self, *args, **kwargs):
        self.system_prompt = f"""
            阅读这篇文章，将它摘要成 150 字以内的报道。报道要讲明白：
            1. 文章来自于哪个媒体
            2. 发生了什么事情
            3. 谁做了这件事情
            4. 事情发生的时间
            5. 事情发生的地点
            6. 事情发生的原因
            7. 事情导致的后果或者可能的后果
            8. 其他与它相关的事情有哪些，是否是一种趋势
            9. 是否有人针对这件事情发表观点
        """
        pass

    def abstract(self, text: str) -> DocAbstractResult:
        abs_ = openai_chat_completion_api(text, self.system_prompt)
        result = DocAbstractResult(
            text=abs_,
            ori_content=text,
        )
        return result


class UrlAbstractor(object):
    def __init__(self, *args, **kwargs):
        # 不一定需要一个单独的 doc abstractor，因为有些厂家的 api 已经支持直接理解 url
        # 当然，他们的做法肯定也是下载网页内容，然后再理解，所以，也可以自己去这么拆开
        self.doc_abstractor = DocAbstractor(*args, **kwargs)
        pass

    @staticmethod
    def get_webpage_text(url: str) -> str:
        # 获取网页内容
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功

        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取所有段落的文本
        paragraphs = soup.find_all('p')  # TODO: 优化提取内容的逻辑
        text = ' '.join([para.get_text() for para in paragraphs])

        return text

    def abstract(self, url: str) -> DocAbstractResult:
        text = self.get_webpage_text(url)
        res = self.doc_abstractor.abstract(text)
        res.url = url
        return res
