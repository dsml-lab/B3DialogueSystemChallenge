import os
import openai
import time

from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)
from langchain.callbacks.base import CallbackManager #langchain==0.0.142
##################################################

from dotenv import load_dotenv, find_dotenv
_=load_dotenv(find_dotenv())
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
##################################################

from src.modules.log_create import LogCreate #ログの生成モジュール（自作モジュール）
logcreate = LogCreate()
##################################################

def to_message(role:str="human", content:str='hello'):
    if role == "system":
        return SystemMessage(content=content)
    elif role == "human":
        return HumanMessage(content=content)
    elif role == "AI":
        return AIMessage(content=content)

class ChatgptClient:
    def __init__(self, model_name='gpt-4', temperture=1):
        self.model_name = model_name
        openai.api_key = OPENAI_API_KEY
        self.llm = ChatOpenAI(openai_api_key=openai.api_key, model_name=model_name, temperature=temperture, streaming=True, verbose=True, callback_manager=CallbackManager(handlers=[]))

    #生成した出力のcontentのみを受け取る関数
    def __get_response_stream_with_pause(self, messages):
        response = self.llm(messages)
        return response.content.strip()
    def send(self, messages:list) -> str:
        begin_time = time.time()
        response = self.__get_response_stream_with_pause(messages)#発話生成
        process_time = time.time() - begin_time
        print("生成時間->", process_time)
        logcreate.log_chatgpt_time(process_time)
        return response

