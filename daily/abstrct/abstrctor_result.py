"""
摘要器、萃取器、压缩器、理解器的结果。
"""

# coding = utf8

from dataclasses import dataclass, field
from typing import List
from pydub import AudioSegment


@dataclass
class DocAbstractResult:
    text: str  # 摘要的结果
    logs: List[str] = field(default_factory=list)  # 一些中间日志
    ori_content: str = ''  # 摘要前的原文，如果有
    url: str = ''  # 原文的链接，如果有


@dataclass
class ReportAbstractResult:
    text: str  # 最终的文章
    audio: AudioSegment = None  # 最终的音频
    logs: List[str] = field(default_factory=list)  # 一些中间日志
    doc_abstract_results: List[DocAbstractResult] = field(default_factory=list)  # 文章摘要的结果列表
