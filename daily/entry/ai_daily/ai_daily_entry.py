"""
AI daily 的入口
"""

# coding = utf8

import os
from typing import List
from daily.abstrct.doc_abstrctor import UrlAbstractor, DocAbstractResult
from daily.abstrct.report_abstrctor import ReportAbstractor, ReportAbstractResult
from daily.api.tts.azure.azure_tts import AzureTTS, TtsInput, TtsOutput
from pybp.logger.app_logger import get_logger

logger = get_logger()


class AiDailyEntry(object):
    def __init__(self, urls: List[str]):
        self.urls = urls
        self.url_abstractor = UrlAbstractor()
        self.report_abstractor = ReportAbstractor()
        pass

    def report(self) -> ReportAbstractResult:
        # 逐个 url 做摘要
        url_res_lst = []  # 各个 url 摘要的结果
        for url in self.urls:
            res = self.url_abstractor.abstract(url)
            url_res_lst.append(res)

        # TODO: 合并 url, 同一个事情的相关文章被放到一起

        # TODO: rank, 和人工调整顺序

        # TODO: 挑选开头，挑选结尾， 删除低优先级新闻(根据时长)

        # TODO: 交由人工做编辑调整

        # 转音频
        tts_handler = AzureTTS()
        audios = []
        for doc_abs in url_res_lst:
            tts_input = TtsInput(doc_abs.text)
            tts_output = tts_handler.tts(tts_input=tts_input)
            audios.append(tts_output)

        report_res = self.report_abstractor.abstract(url_res_lst, audios)
        return report_res

    def dump(
            self,
            daily_result: ReportAbstractResult,
            out_dir: str,
            internal_dir: str = '',
    ):
        """ 将 report 最终保存下来

        Args:
            daily_result: report 的内容
            out_dir: 输出目录
            internal_dir: 中间结果的输出目录
        """

        # report 文本输出路径
        report_text_path = os.path.join(out_dir, 'report.txt')
        # report 文本输出
        with open(report_text_path, 'w', encoding='utf-8') as outs:
            outs.write(daily_result.text)
        logger.info(f'report text is dump into {report_text_path}')

        # report 音频输出路径
        report_audio_path = os.path.join(out_dir, 'report.wav')
        daily_result.audio.export(report_audio_path, format='wav')
        logger.info(f'report audio is dump into {report_audio_path}')
