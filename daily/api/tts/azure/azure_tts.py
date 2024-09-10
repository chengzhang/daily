"""

"""

from io import BytesIO
from pydub import AudioSegment
import os
from typing import Dict, Optional
import pandas as pd
import azure.cognitiveservices.speech as speechsdk
from daily.api.tts.tts_interface import TtsInput, TtsOutput, TtsInterface


class SupportedVoices:
    _inst: 'SupportedVoices' = None

    def __init__(self, data_frame: pd.DataFrame, *args, **kwargs):
        self.data_frame = data_frame
        self.speaker_to_voice_name: Dict[str: str] = {}
        self.parse_df()

    def parse_df(self):
        for i, row in self.data_frame.iterrows():
            self.speaker_to_voice_name[row['name']] = row['voice_name']

    """
    def __new__(cls, *args, **kwargs):
        if not cls._inst:
            cls._inst = cls.from_csv()
        return cls._inst
    """

    @classmethod
    def from_csv(cls, csv_file: str = None):
        if not csv_file: 
            current_dir = os.path.dirname(os.path.abspath(__file__))
            csv_file = os.path.join(current_dir, 'supported_voices.csv')
        df = pd.read_csv(csv_file, sep=',')
        return cls(data_frame=df)

    def get_voice_name(self, speaker='云健', role='', style=''):
        return self.speaker_to_voice_name[speaker]


class AzureTTS(TtsInterface):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.speech_key = os.getenv('AZURE_SPEECH_KEY')
        self.service_region = "eastus"
        self.supported_voices = SupportedVoices.from_csv()

    def tts(self, tts_input: TtsInput) -> Optional[TtsOutput]:
        """
        :return:
        TODO: 加一个 cache 的模块来缓存
        """
        # if not wav_file:
        #     wav_file = f'tmp/{abs(hash(text))}.wav'
        # Creates an instance of a speech config with specified subscription key and service region.
        speaker = tts_input.voice_name
        speech_config = speechsdk.SpeechConfig(subscription=self.speech_key, region=self.service_region)
        # Note: the voice setting will not overwrite the voice element in input SSML.
        # speech_config.speech_synthesis_voice_name = "zh-CN-XiaohanYanli"
        voice_name_ = self.supported_voices.get_voice_name(speaker)
        speech_config.speech_synthesis_voice_name = voice_name_
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        # text = "你好，这是晓晓。"
        text = tts_input.text
        result = speech_synthesizer.speak_text_async(text).get()
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech synthesized for text [{}]".format(text))
        if result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                print("Error details: {}".format(cancellation_details.error_details))
            return None
            
        audio_stream = BytesIO(result.audio_data)
        audio_segment = AudioSegment.from_wav(audio_stream)
        if tts_input.out_audio_file:
            audio_segment.export(tts_input.out_audio_file, format="wav")

        # ad_stream = speechsdk.AudioDataStream(result=result)
        # ad_stream.save_to_wav_file(wav_file)

        output = TtsOutput(audio_segment, input=tts_input)
        return output


if __name__ == '__main__':
    tts = AzureTTS()
    ad_seg = tts.tts('四季度以来，商业银行推广个人养老金开户的粒度持续加大')
    ad_seg.export("tmp/audio.wav", format="wav")
