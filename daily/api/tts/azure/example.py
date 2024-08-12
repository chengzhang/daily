'''
  For more samples please visit https://github.com/Azure-Samples/cognitive-services-speech-sdk
'''
import pdb

import azure.cognitiveservices.speech as speechsdk

# Creates an instance of a speech config with specified subscription key and service region.
speech_key = "82fb49572ba048b9ba9e6196fd811d2a"
service_region = "eastus"

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
# Note: the voice setting will not overwrite the voice element in input SSML.
# speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"
speech_config.speech_synthesis_voice_name = "zh-CN-XiaohanYanli"

text = "你好，这是晓晓。"

# use the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

result = speech_synthesizer.speak_text_async(text).get()
# Check result
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        print("Error details: {}".format(cancellation_details.error_details))
ad_stream = speechsdk.AudioDataStream(result=result)
ad_stream.save_to_wav_file('tmp/azure_tts_result_example.wav')
