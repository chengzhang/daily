"""
报道摘要器、萃取器、压缩器、理解器。理解一系列文章、url。
"""

# coding = utf8

from typing import List
from daily.abstrct.abstrctor_result import DocAbstractResult, ReportAbstractResult
from daily.api.tts.tts_interface import TtsOutput
from pydub import AudioSegment
from pybp.logger.app_logger import get_logger

logger = get_logger()


class ReportAbstractor(object):
    def __init__(self):
        pass

    def abstract(self, doc_abstract_results: List[DocAbstractResult], audios: List[TtsOutput]) -> ReportAbstractResult:
        final_text = self.merge_articles(doc_abstract_results)
        final_audio = self.concat_audios([x.audio for x in audios])
        return ReportAbstractResult(
            text=final_text,
            audio=final_audio,
            doc_abstract_results=doc_abstract_results,
        )

    def merge_articles(self, doc_abs_results: List[DocAbstractResult]) -> str:
        res_text = ''
        for i, doc in enumerate(doc_abs_results):
            res_text += f"""
            # - {i+1} - 
                {doc.text} 
            """

        # 添加参考链接
        res_text += '# - ref -'
        for i, doc in enumerate(doc_abs_results):
            res_text += f"""
            {i+1}. {doc.url} 
            """
        return res_text


    def concat_audios(self, audios: List[AudioSegment], silence_duration=1000) -> AudioSegment:
        if not audios:
            logger.warning(f'empty audio list')
            return AudioSegment.empty()
        res_audio = audios[0]
        for seg in audios[1:]:
            res_audio += AudioSegment.silent(duration=silence_duration)
            res_audio += seg
        return res_audio

