# roopディレクトリへ移動
def sys_path_to_root():
    import os, sys
    ROOT_PATH = '../' # Module/
    # スクリプトのディレクトリパスを取得
    script_directory = os.path.dirname(os.path.abspath(__file__))
    # rootディレクトリのパスを計算
    root_directory = os.path.abspath(os.path.join(script_directory, ROOT_PATH))
    sys.path.append(root_directory)
sys_path_to_root()

import json # JSONを扱うためのモジュール
import time

from Module.communicator import Communicator # 親クラス
# コンソールで実行するときは以下のimport文をアンコメント
#from communicator import Communicator

class SpeechGenerator(Communicator):
    """
    音声合成API(Docomo TTS)を使うためのクラス
    Attributes:
        hostname (str): ホスト名
        port (int): ポート番号
    """
    def __init__(self, hostname, port):
        """
        Args:
            hostname (str): ホスト名
            port (int): ポート番号
        """
        # 与えられたホスト名, ポート名でSocket通信のクライアントを作成
        super().__init__(hostname, port)
        self.is_speaking = False


    def say(self, content, pitch=110, speed=100, volume=100):
        """
        音声合成サーバにJSON形式のデータを送信し, 音声を再生させる関数
        Args:
            content (str): 再生させたい内容の文字列
        Returns:
            None
        """
        if not self.client.connected:
            return

        cmd = self.create_speech_command(content, pitch, speed, volume) # JSON形式のデータを作成
        self.is_speaking = True
        self.client.send(cmd) # 作成したJSONデータをサーバへ送信

        # 再生中か停止中か確認し, 再生中ならループ
        while self.is_speaking:
            time.sleep(0.1) # 音声が再生されていれば100ミリ秒待機


    def create_speech_command(self, content, pitch, speed, volume):
        """
        音声合成サーバに音声を再生させるためのJSONオブジェクトを作成する関数
        デフォルト：pitch=150, speed=115, volume=100
        Args:
            content (str): 再生させたい内容の文字列
        Returns:
            cmd (str): 辞書から整形したJSON形式の文字列
        """
        """ cmd = dict() # 空の辞書作成
        cmd['engine'] = 'HOYA' # どんな音声合成APIを使うか. 'engine'キーに'HOYA'という値を入力
        cmd['speaker'] = 'hikari' # 話者名. 'speaker'キーに'hikari'という値を入力
        cmd['text'] = content # 合成するテキスト. 'text'キーにcontentに格納された値を入力
        # cmd['emotion'] = 'happiness' # 感情カテゴリの指定.
        # cmd['emotion_level'] = 2 # 感情レベルの指定. 1 or 2
        cmd['pitch'] = pitch # 音声のピッチを上下
        cmd['speed'] = speed # 喋るスピード
        cmd['volume'] = volume # 音声の音量上下
        cmd = json.dumps(cmd) # 辞書をJSON形式の文字列に変換 """
        cmd = dict() # 空の辞書作成
        cmd['engine'] = 'POLLY' # どんな音声合成APIを使うか. 'engine'キーに'HOYA'という値を入力
        cmd['speaker'] = 'Mizuki' # 話者名. 'speaker'キーに'hikari'という値を入力
        cmd['pitch'] = pitch # 音声のピッチを上下
        cmd['volume'] = volume # 音声の音量上下
        cmd['speed'] = speed # 喋るスピード
        cmd['vocal-tract-length'] = 0 #AmazonPollyから追加
        cmd['duration-information'] = False #AmazonPollyから追加
        cmd['speechmark'] = False #AmazonPollyから追加
        cmd['text'] = content # 合成するテキスト. 'text'キーにcontentに格納された値を入力
        cmd = json.dumps(cmd) # 辞書をJSON形式の文字列に変換
        return cmd

    def say_cmd(self, content, pitch=110, speed=100, volume=100):
        """
        音声合成サーバにJSON形式のデータを送信し, 音声を再生させる関数
        Args:
            content (str): 再生させたい内容の文字列
        Returns:
            None
        """
        if not self.client.connected:
            return

        cmd = self.create_speech_command(content, pitch, speed, volume) # JSON形式のデータを作成
        return cmd


    def on_received(self, message):
        """
        常に動いている関数
        Args:
            message(str): サーバから受信した文字列
        Returns:
        """
        recv_result = json.loads(message) # 受信したjsonデータを読み込む
        result = recv_result['result'] # 受信データのresult部分を確認

        # resultの内容がsuccess-endならループから抜ける
        if result == 'success-end':
            self.is_speaking = False

        # resultの内容がfailedならエラーが発生している状態なので, ループから抜ける
        elif result == 'failed':
            print('speech generate process failed.')
            self.is_speaking = False


# コンソール上で実行するときには以下が実行される.
if __name__ == '__main__':
    #hostname, port = 'localhost', 3456 # ホスト名, ポート番号を設定
    #hostname, port = '133.14.215.8', 1234 # ホスト名, ポート番号を設定
    #hostname, port = '133.14.214.124', 1234 # ホスト名, ポート番号を設定
    #import pdb; pdb.set_trace()
    hostname, port = '192.168.0.5', 3456 # ホスト名, ポート番号を設定
    speech_generator = SpeechGenerator(hostname, port) # ホスト名, ポート番号を指定し, オブジェクトを作成
    speech_generator.start() # Socket通信を開始
    print('start')
    speech_generator.say('システムを起動しました') # 再生させたい内容の文字列をsay関数に渡す
    speech_generator.stop() # Socket通信を停止