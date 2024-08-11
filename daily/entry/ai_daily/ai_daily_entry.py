"""
AI daily 的入口
"""

# coding = utf8

from typing import List
from daily.abstrct.doc_abstrctor import UrlAbstractor, DocAbstractResult
from daily.abstrct.report_abstrctor import ReportAbstractor, ReportAbstractResult


class AiDailyEntry(object):
    def __init__(self, urls: List[str]):
        self.urls = urls
        self.url_abstractor = UrlAbstractor()
        self.report_abstractor = ReportAbstractor()
        pass

    def report(self) -> ReportAbstractResult:
        url_res_lst = []  # 各个 url 摘要的结果
        for url in self.urls:
            res = self.url_abstractor.abstract(url)
            url_res_lst.append(res)
        report_res = self.report_abstractor.abstract(url_res_lst)
        return report_res
