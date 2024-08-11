"""
报道摘要器、萃取器、压缩器、理解器。理解一系列文章、url。
"""

# coding = utf8

from typing import List
from daily.abstrct.abstrctor_result import DocAbstractResult, ReportAbstractResult


class ReportAbstractor(object):
    def __init__(self):
        pass

    def abstract(self, doc_abstract_results: List[DocAbstractResult]) -> ReportAbstractResult:
        text = f'''
        这里共计 {len(doc_abstract_results)} 篇文章
        '''
        return ReportAbstractResult(text=text, doc_abstract_results=doc_abstract_results)

