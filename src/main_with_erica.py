# rootディレクトリへ移動
def sys_path_to_root():
    import os, sys
    ROOT_PATH = '../' # src/ rootディレクトリへの相対パス
    # スクリプトのディレクトリパスを取得
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # rootディレクトリのパスを計算
    root_directory = os.path.abspath(os.path.join(script_directory, ROOT_PATH))
    sys.path.append(root_directory)
sys_path_to_root()

import time
import sys

#発話生成，対話履歴保存周りのモジュール（自作モジュール）
from src.modules.chatgpt_client import ChatgptClient
from src.modules.memory import Memory

#ログの生成モジュール（自作モジュール）
from src.modules.log_create import LogCreate

#エージェント周りのモジュール(コンペ共通モジュール)import
from Module.speech_generator import SpeechGenerator
from Module.speech_recognition_manager import SpeechRecognitionManager
from Module.oculus_lip_sync import OculusLipSync
from Module.robot_body_controller import RobotBodyController
from Module.robot_expression_controller import RobotExpressionController

# 音声合成のパラメータ設定
pitch = 110 # amazon pollyデフォルト音程は110
speed = 105 # amazon pollyデフォルト話速は105
volume = 100 # amazon pollyデフォルト音量は100

# 通信ポート指定
expression_generator = RobotExpressionController("localhost", 20000)
motion_generator =RobotBodyController("localhost", 21000)
speech_generator = SpeechGenerator("localhost", 3456)
speech_recognition_manager = SpeechRecognitionManager("localhost", 8888)
oculus_lip_sync = OculusLipSync("localhost", 31000)

# ログモジュールのオブジェクトを作成
logcreate = LogCreate()

#エージェントの発話
def say(text, pitch=pitch, speed=speed, volume=volume):
    time.sleep(0.01)
    speech_generator.say(text, pitch, speed, volume)
    print(text)
    logcreate.log_say(text)

# 音声認識
def hear():
    speech_recognition_manager.client.send('start')# 音声認識を開始するためにサーバへ送信するコマンド 
    message = speech_recognition_manager.read_result() # 音声認識
    speech_recognition_manager.client.send('stop') # 音声認識を停止するためにサーバへ送信するコマンド
    if message:
        logcreate.log_hear(message)
        return message
    else:
        print('Error message is Nonetype')

# 表情生成用の関数
def robot_face(name):
    expression_generator.set_expression(name)

# 視線制御用の関数
def robot_gaze(x, y, z):
    motion_generator.set_gaze(x, y, z)

# 姿勢制御用の関数
def robot_motion(motion):
    motion_generator.play_motion(motion)

# システム開始時の処理
def start():
    speech_generator.start()
    motion_generator.start()
    expression_generator.start()
    speech_recognition_manager.start()
    speech_recognition_manager.client.send('stop')

# システム終了時の処理
def stop():
    speech_generator.stop()
    motion_generator.stop()
    expression_generator.stop()
    speech_recognition_manager.stop()
    sys.exit()

#表情をパラメータで指定
def set_robot_params(valence, arousal, dominance, realintention):
    cmd = expression_generator.create_paramater('valence', valence)
    expression_generator.send_cmd(cmd)
    cmd = expression_generator.create_paramater('arousal', arousal)
    expression_generator.send_cmd(cmd)
    cmd = expression_generator.create_paramater('dominance', dominance)
    expression_generator.send_cmd(cmd)
    cmd = expression_generator.create_paramater('realintention', realintention)
    expression_generator.send_cmd(cmd)

# デフォルトの姿勢(CGエリカを使う場合)
def default_pause():
    # 右手を膝に
    robot_motion('right_hand_carefullyonknee')
    # 左手を膝に
    robot_motion('left_hand_carefullyonknee')
    # 視線を正面に
    robot_gaze(0, 1.2, 1.5)
    # スリープ
    time.sleep(3)


prompt = """
# 条件
ユーザとお話ししてください。
"""

def main():
    client = ChatgptClient()
    memory = Memory()
    default_pause() # デフォルトの姿勢
    robot_gaze(0, 1.2, 1.5) # 視線を正面に

    robot_face('MoodBasedFACS') # 表情
    logcreate.log_start_time()
    logcreate.log_prompt(prompt)
    messages = memory.add("system", prompt)
    response = client.send(messages) # システム発話（挨拶）の生成
    start = time.time()
    
    robot_motion('greeting_deep') # お辞儀
    time.sleep(0.2)
    set_robot_params(0.2, 0.1, 0, 0)
    
    robot_gaze(0, 1.2, 1.5) # 視線を正面に
    time.sleep(2.5)
    
    say(response)
    
    # 発話ターンの受け渡しを示す振る舞い
    time.sleep(0.0)
    robot_motion('greeting_deep_spine')
    robot_gaze(0, 1.2, 1.5) # 視線を正面に
    
    messages = memory.add("AI", response) # システム発話をメモリに格納

    while True:
        robot_face('fullsmile') # 表情(笑顔)
        user_input = hear() # ユーザ発話

        # うなずき３回
        robot_motion('nod_deep')
        time.sleep(0.5)
        robot_motion('nod_deep')
        time.sleep(0.8)
        robot_motion('nod_deep')
        robot_gaze(0, 1.2, 1.5) # 視線を正面に
        
        messages = memory.add("human", user_input) # ユーザ発話をメモリに格納
        current_tme = time.time() # 現時点の時刻を取得
        process_time = current_tme - start#処理時刻を取得
        print(f"time:{process_time}")

        response = client.send(messages) # システム発話（挨拶）の生成
        robot_face('MoodBasedFACS') # 表情
        say(response) # システム発話

        #発話ターンの受け渡しを示す振る舞い
        time.sleep(0.0)
        robot_motion('greeting_deep_spine')
        robot_gaze(0, 1.2, 1.5) # 視線を正面に

        messages = memory.add("AI", response) # システム発話をメモリに格納

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
        sys.exit()

    except Exception:
        import traceback
        traceback.print_exc() # 全てのエラー文をターミナルに表示
        logcreate.log_error(traceback.format_exc()) # ログファイルにエラー文を記述
        stop() # 各モジュールのTCP通信の終了
        sys.exit()

    # 正常終了時の処理
    else:
        stop() # 各モジュールのTCP通信の終了
