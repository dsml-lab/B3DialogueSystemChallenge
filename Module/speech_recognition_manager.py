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

import threading

from Module.communicator import Communicator # 親クラス
# コンソールで実行するときは以下のimport文をアンコメント
#from DialogueCompetition.modules.communicator import Communicator
# https://drive.google.com/drive/folders/1guLs0fYzSaFe5nTNV1ikTARgPacP0a4Q
# https://hil-erica.github.io/GoogleSpeechAPI/speech_recognition.html


class SpeechRecognitionManager(Communicator):
    """
    音声認識API(Google Speech Recognition Server)を使うためのクラス

    Args:
        hostname (str): ホスト名
        port (int): ポート番号
    """
    def __init__(self, hostname, port):
        super().__init__(hostname, port)
        self.recognition_result = '' # 音声認識結果を格納するための変数

        # 音声認識結果を格納するリスト
        self.recognition_results = []
        self.interim_results=[]

        # 認識途中を格納する変数
        self._interimresult = ''


    def start(self):
        """
        Socket通信を開始するための関数

        Args:
            None

        Returns:
            None
        """
        super().start() # Socket通信を開始.
        self.FLAG = True
        self.client.send('start') # 音声認識を開始するためにサーバへ送信するコマンド


    def stop(self):
        """
        Socket通信を停止するための関数

        Args:
            None

        Returns:
            None
        """
        self.client.send('stop') # 音声認識を停止するためにサーバへ送信するコマンド
        #self.recognition_result = ''
        super().stop() # Socket通信の停止


    def read_result(self):
        """
        音声認識結果を取得

        Args:
            None

        Returns:
            tmp(str): 音声認識結果
        """
        tmp = ''
        while True:
            if self.recognition_result:
                tmp = self.recognition_result
                self.recognition_result = ''
                break
                
        return tmp


    @property
    def result_count(self):
        return len(self.recognition_results)
    
    def get_interimresult(self):
        """途中結果を取得する"""

        # これをしないと，遅れて確定したものが次の質問の回答になることがある
        self.client.send('stop')

        # 初期化しないと前回の結果が残り続ける
        tmp = self._interimresult
        self._interimresult = ''
        print('ASR(interimresult):', tmp)
        return tmp

    def get_interimresults(self):
        """途中結果を取得する（複数の途中結果を取得）"""

        # これをしないと，遅れて確定したものが次の質問の回答になることがある
        self.client.send('stop')

        # 初期化しないと前回の結果が残り続ける
        tmp = self.interim_results
        self.interim_results = []
        print('ASR(interim_results):')
        print(tmp) # list型の格納であることに注意
        return tmp


    def on_received(self, message):
        """
        messageが送られてきたときの処理

        Args:
            message(str): 受信したメッセージ

        Returns:
            None
        """

        recv_result = message.split('\n') # サーバからの音声認識結果を受信, \nでリスト化. (途中結果や認識率も受信し, \nで分かれている)
        interimresult = [x for x in recv_result if x.startswith('interimresult:')] # 先頭が'interimresult:'のリストの要素を抽出
        result = [x for x in recv_result if x.startswith('result:')] # 先頭が'result:'のリストの要素を抽出
        # print(interimresult)
        # print(result)
        # resultが存在するなら変数に格納
        if result:
            # self.recognition_result = result[0][7:]
            # print('ASR: ' + self.recognition_result)
            self.recognition_results.append(result[0][7:])
            print(f'ASR({self.result_count}): {self.recognition_results[-1]}')

            # 音声認識が確定したら，認識途中のものを初期化
            self._interimresult = ''
            # 音声認識結果を格納
            self.recognition_result = self.recognition_results[-1]
        # interimresultが存在するなら変数に格納
        if interimresult:
            self._interimresult = interimresult[0][14:]
            self.interim_results.append(self._interimresult)


# コンソール上で実行するときには以下が実行される.
if __name__ == "__main__":
    hostname, port = 'localhost', 8888 # ホスト名, ポート番号を設定
    speech_recognition_manager = SpeechRecognitionManager(hostname, port) # ホスト名, ポート番号を指定し, オブジェクトを作成
    speech_recognition_manager.start() # Socket通信を開始
    # import pdb; pdb.set_trace()
    # 無限ループ. 音声認識結果に終了という文字が入っていればループから抜ける
    try:
        while True:
            result = speech_recognition_manager.read_result() # 音声認識結果を受信

            if '終了' in result:
                break
    finally:
        speech_recognition_manager.stop() # Socket通信の終了
        print('end')