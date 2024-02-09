# rootディレクトリへ移動
def sys_path_to_root():
    import os, sys
    ROOT_PATH = '../' # src rootディレクトリへの相対パス
    # スクリプトのディレクトリパスを取得
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # rootディレクトリのパスを計算
    root_directory = os.path.abspath(os.path.join(script_directory, ROOT_PATH))
    sys.path.append(root_directory)
sys_path_to_root()

import time
import sys

#発話生成，対話履歴保存周りのモジュール（自作モジュール）
# from src.modules.chatgpt_client import ChatgptClient
# from src.modules.memory import Memory
from src.modules.gpt_utils import *

#ログの生成モジュール（自作モジュール）
from src.modules.log_create import LogCreate

# ログモジュールのオブジェクトを作成
logcreate = LogCreate()

#エージェントの発話
def say(text):
    print('システム発話:', text)
    logcreate.log_say(text)

# 音声認識
def hear():
    message = input('ユーザー発話: ')
    if message:
        logcreate.log_hear(message)
        return message
    else:
        print('Error message is Nonetype')

# システム開始時の処理
def start():
    pass

# システム終了時の処理
def stop():
    sys.exit()

prompt = """
# 条件
あなたの目的はユーザーと楽しく会話することです。
最初に挨拶をして、名前を聞いてください。
"""

def main():
    messages = []

    logcreate.log_start_time()
    logcreate.log_prompt(prompt)

    messages.append(create_message(ROLE.SYSTEM, prompt)) # 命令プロンプト

    response = get_response(messages, model='gpt-4-0125-preview') # システム発話（挨拶）の生成
    say(response)
    messages.append(create_message(ROLE.ASSISTANT, response)) # システム発話をメモリに格納

    while True:
        user_input = hear() # ユーザ発話
        messages.append(create_message(ROLE.USER, user_input)) # ユーザ発話をメモリに格納

        response = get_response(messages, model='gpt-4-0125-preview') # システム発話（挨拶）の生成
        say(response) # システム発話
        messages.append(create_message(ROLE.ASSISTANT, response)) # システム発話をメモリに格納

if __name__ == '__main__':
    start() # 各モジュールのTCP通信の開始

    # エラーが起きた時でもTCP通信を正常に終了させるためのtry文
    try:
        main() # シナリオ開始

    except KeyboardInterrupt:
        import traceback
        traceback.print_exc() # ctrl+C時のエラー文をターミナルに表示
        logcreate.log_error(traceback.format_exc()) # ログファイルにエラー文を記述
        stop() # 各モジュールのTCP通信の終了

    except Exception:
        import traceback
        traceback.print_exc() # 全てのエラー文をターミナルに表示
        logcreate.log_error(traceback.format_exc()) # ログファイルにエラー文を記述
        stop() # 各モジュールのTCP通信の終了

    # 正常終了時の処理
    else:
        stop() # 各モジュールのTCP通信の終了
