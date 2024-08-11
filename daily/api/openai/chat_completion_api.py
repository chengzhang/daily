"""
提供 openai 的接口

TODO:
  - 建立一个repo专门用来管理所有 aigc api
  - 让所有这些参数进入配置单
"""

import os
import openai
openai.api_type = "azure"
openai.api_base = "https://deliver8.openai.azure.com/"
openai.api_version = "2024-02-15-preview"
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = "2e40a7b847aa487ca40c30bda3b931a0"

"""
response = openai.ChatCompletion.create(
  engine="gpt-4o",
  messages = [{"role":"system","content":"You are an AI assistant that helps people find information."},{"role":"user","content":"hello"},{"role":"assistant","content":"Hello! How can I assist you today?"}],
  temperature=0.7,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None)
"""


def openai_chat_completion_api(
        query: str,
        system_prompt: str = 'You are an AI assistant that helps people find information.'
):
    response = openai.ChatCompletion.create(
        engine="gpt-4o",
        messages=[
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": query},
        ],
        temperature=0.7,
        max_tokens=800,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    answer = response['choices'][0]['message']['content']
    return answer


if __name__ == '__main__':
    answer = openai_chat_completion_api('你好')
    print(answer)
