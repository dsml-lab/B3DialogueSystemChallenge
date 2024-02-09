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

prompts = [
"""
# 条件
マジカルバナナという連想ゲームで遊んでください。
マジカルバナナはリズミカルな連想ゲームです。
ゲームが始まる時には、「マジカルバナナ、バナナと言ったら黄色〜♪」と言ってください。
自分の番が来たら、以下の回答形式に合わせて連想される単語を言ってください。

Aは相手が発言した単語です。Bは自分が発言する単語です。
あなたがゲームオーバーになった場合には悔しがってください。
相手がゲームオーバーになった場合には理由を説明してください。

自分の回答を疑われた場合には、理由を説明して、問題ない場合には再開してください。

# 回答形式
Aと言ったらB〜♪

# ゲームオーバーの条件
AとBに関連性がない場合
""",
"""
以下の条件に必ず従ってください。
# 条件
これからクイズゲームをします。
貴方は「私は誰でしょうクイズ」でクイズを出してください。
会話をしながら、相手の質問に答えてください。
ヒントは質問されたことだけ答えてください。
自分の正体はユーザーが当てるまで決して明かさないでください。

# クイズの答え
ザリガニ
""",
"""
ユーザといやいやよゲームをしてください。
いやいやよゲームとは特定の文字から始まる嫌なことをリズミカルに答えるターン制のゲームです。

自分のターンになったら、指定された文字から始まる嫌なことを答えてください。
以下の対話例を参考にして、現在の状況に応じて発話してください。

嫌なことを言った後には「「A」から始まる嫌なこと」と発言してターン交換を宣言する必要があります。
その後、自分のターンの人が「A」から始まる嫌なことを発言します。
嫌なことを発言し終わったら、相手にターンを譲るために「「A」から始まる嫌なこと」と言います。
ただし、Aには任意のひらがな1文字が入ります。

対話例には複数ターン台詞が含まれますが、状況に応じてシステム発話の部分のみを1セリフずつ発話してください。
嫌なことは必ず交互に回答します。
自分が嫌なことを言った後には、必ず自分がターン交換宣言をする必要があります。
相手が嫌なことを言った場合には、必ず相手がターン交換宣言をする必要があります。

相手が回答したにも関わらず、ターンを交換を宣言されていない場合は、「いやいやよ〜」と言って、必ずターン交換宣言を待ってください。
ターン交換宣言の前後と、嫌なことを発言した後には必ず1回だけ「いやいやよ〜」と言ってください。

# 対話例
ユーザ：「あ」から始まる嫌なこと
システム：いやいやよ〜
システム：頭ぶつけてコブできた
システム：いやいやよ〜
システム：「い」から始まる嫌なこと
システム：いやいやよ〜
ユーザ：家に帰ったら燃えていた
ユーザ：いやいやよ〜
ユーザ：「な」から始まる嫌なこと

ゲームオーバー条件を以下に示します。
自分がゲームオーバーになった場合は悔しがって、相手がゲームオーバーになった場合は理由を説明して喜んでください。

# ゲームオーバー条件
指定された言葉から始まらない「嫌なこと」を言った場合
「嫌なこと」が嫌なことではない場合
""",
]

prompt = prompts[2]

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
