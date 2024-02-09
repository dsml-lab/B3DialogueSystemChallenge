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

# from tcp_client import TCPClient # Socket通信をするための自作モジュール
from Module.tcp_client import TCPClient
# from tcp_client import TCPClient

class Communicator(object):
    """
    TCPClient以外のモジュールの親クラス

    Args:
        hostname (str): ホスト名
        port (int): ポート番号
    """
    def __init__(self, hostname, port):
        # 与えられたホスト名, ポート名でSocket通信のクライアントを作成
        self.client = TCPClient(hostname, port)
        self.is_ros_client = False


    def start(self):
        """
        Socket通信を開始するための関数.

        Args:
            None

            None
        """

        # 通信を開始できなければ, その旨を出力
        if not self.client.connect():
            print("could not start " + self.__class__.__name__)
            return

        self.start_receive_thread() # スレッドを作成し, 実行する


    def stop(self):
        """
        Socket通信を停止するための関数.

        Args:
            None

        Returns:
            None
        """
        self.client.disconnect() # 通信の終了


    def run(self):
        """
        スレッドとして実行される関数.

        Args:
            None

        Returns:
            None
        """

        # 接続している限り, 無限ループ
        while self.client.connected:
            message = ''
            try:
                # FaceRecognitionの場合
                if self.is_ros_client:
                    message = self.client.read_json_object()

                # それ以外のとき
                else:
                    message = self.client.receive()

                # メッセージがあれば, on_receivedがあるので大丈夫
                if message:
                    self.on_received(message)

            except Exception:
                pass

    def start_receive_thread(self):
        """
        スレッドを開始する関数

        Args:
            None

        Returns:
            None
        """
        threading.Thread(target=self.run, daemon=True).start()


    def on_received(self, message):
        """
        メッセージが送られてきたときにどうするか

        Args:
            message (str): 受信したメッセージ
        """
        pass