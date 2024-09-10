"""
tts result data struct
"""

# coding = utf8

from dataclasses import dataclass
from pydub import AudioSegment


@dataclass
class TtsInput:
    text: str  # 文本
    voice_name: str = ''  # tts 音色
    speed: float = 1.0  # tts 语速
    out_audio_file: str = ''  # 输出路径
    pass


@dataclass
class TtsOutput:
    audio: AudioSegment  # 音频
    input: TtsInput  # 请求
    pass


class TtsInterface:
    def __init__(self):
        pass

    def tts(self, tts_input: TtsInput) -> TtsOutput:
        pass
