import openai
import os
import json
from typing import Callable, List, Any

GPT_DEFAULT_MODEL = 'gpt-3.5-turbo'

class ROLE:
    SYSTEM = 'system'
    ASSISTANT = 'assistant'
    USER = 'user'

def get_openai_api_key():
    return os.environ['OPENAI_API_KEY']

def create_message(role: str, content: str):
    return {'role': role, 'content': content}

def get_response_stream(messages:List[dict], callback:Callable[[str], None], model=GPT_DEFAULT_MODEL, functions_dict=None, function_callbacks:List[Callable[[dict], None]]=[], temperature=0.7) -> str:
    responses = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        stream = True,
        functions = functions_dict,
        temperature = temperature,
    )

    message = ''
    for response in responses:
        response_msg = response['choices'][0]['delta']
        chunk = response_msg.get('content')

        if (response_msg.get('function_call') and response_msg['function_call'].get('name')):
            function_name = response_msg['function_call']['name']
            function_args = json.loads(response_msg['function_call']['arguments'] or '{}')
            for i, f in enumerate(functions_dict):
                if function_name == f['name']:
                    function_callbacks[i](function_args)
        if (chunk == None):
            pass
        else:
            message += chunk
            if callback != None:
                callback(chunk)
    
    return message.strip()

def get_response(messages:List[dict], model=GPT_DEFAULT_MODEL, functions_dict=None, function_callbacks:List[Callable[[dict], None]]=[], temperature=0.7) -> str:
    response = openai.ChatCompletion.create(
        model = model,
        messages = messages,
        functions = functions_dict,
        # function_call = 'auto',
        temperature = temperature,
    )

    # TODO: function_calling未実装
    message = response['choices'][0]['message']['content']

    return message.strip()

openai.api_key = get_openai_api_key()

if __name__ == '__main__':
    import time

    wait_sec = 3

    while True:
        # 質問入力プロンプト
        user_input = input("\nChatGPTへの質問入力(Enterで終了):")
        if not user_input:
            break

        # メッセージを作成
        messages = [create_message('user', user_input)]

        # 逐次出力
        print("\nChatGPTの回答を逐次出力")

        response = get_response_stream(messages, callback=lambda x : print(x, end='', flush=True))
        # print('\n', response)

        # API待機時間
        time.sleep(wait_sec)

        # まとめて出力
        print("\nChatGPTの回答をまとめて出力 ↓↓↓")

        response = get_response(messages)
        print(response)

        # API待機時間
        time.sleep(wait_sec)