# rootディレクトリへ移動
def sys_path_to_root():
    import os, sys
    ROOT_PATH = '../../' # src/tools rootディレクトリへの相対パス
    # スクリプトのディレクトリパスを取得
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # rootディレクトリのパスを計算
    root_directory = os.path.abspath(os.path.join(script_directory, ROOT_PATH))
    sys.path.append(root_directory)
sys_path_to_root()

from datetime import datetime
import os
import time

class LogCreate():
    def __init__(self):
        nowdate = datetime.now()
        os.makedirs('logs', exist_ok=True)
        self.log_file = 'logs/{0:%Y%m%d%H%M%S}_TravelAgentGPT_log.txt'.format(nowdate) # 取得した現在時間を対話ログのファイル名にする
        self.start_time = 0
        self.say_num = 0
        self.hear_num = 0
    
    def log_start_time(self):
        self.start_time = time.time()

    # プロンプトをファイルに追記
    def log_prompt(self, prompt):
        with open(self.log_file, mode='a', encoding='utf-8') as f:
            f.write(f'"""プロンプト"""{prompt}\n\n')
    
    # 生成時間をファイルに追記
    def log_chatgpt_time(self, process_time):
        with open(self.log_file, mode='a', encoding='utf-8') as f:
            f.write(f'生成時間->{process_time}\n')

    # 経過時間を取得できる関数
    def get_process_time(self):
        return time.time() - self.start_time

    # システムの発話をファイルに追記
    def log_say(self, text):
        p_time = self.get_process_time()
        min = int(p_time / 60) # 経過時間の分を用意
        sec = int(p_time % 60) # 経過時間の秒を用意
        self.say_num += 1
        with open(self.log_file, mode='a', encoding='utf-8') as f:
            f.write(f'"""システム発話{self.say_num}"""\n {text} {min}:{sec}\n\n') # 末尾に対話開始から発話を始めた時間を記述

    # ユーザの発話をファイルに追記
    def log_hear(self, text):
        p_time = self.get_process_time()
        min = int(p_time / 60) # 経過時間の分を用意
        sec = int(p_time % 60) # 経過時間の秒を用意
        self.hear_num += 1
        with open(self.log_file, mode='a', encoding='utf-8') as f:
            f.write(f'"""ユーザ発話{self.hear_num}"""\n {text} {min}:{sec}\n\n') # 末尾に対話開始から発話を始めた時間を記述

    # エラーログをファイルに追記
    def log_error(self, error_text):
        with open(self.log_file, mode='a', encoding='utf-8') as f:
            f.write(error_text)
