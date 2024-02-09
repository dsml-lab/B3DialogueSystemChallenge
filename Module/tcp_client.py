import socket # Socket通信を行うためのモジュール
import re


class TCPClient():
    """
    Socket通信のクライアントクラス

    Args:
        hostname (str): ホスト名
        port (int): ポート番号
    """
    def __init__(self, hostname, port):
        self.hostname = hostname # ホスト名
        self.port = port # ポート番号
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # socket通信のクライアント
        self.connected = False # 接続確認


    def connect(self):
        """
        socket通信を開始する関数

        Args:
            None

        Returns:
            (boolean): socket通信を開始できればTrue, 失敗したらFalseを返す
        """
        try:
            self.client.connect((self.hostname, self.port)) # ソケット通信を指定したホスト名, ポート番号で開始
        except:
            print('fail to connect ' + self.hostname + '/' + str(self.port))
            return False

        self.connected = True
        return True


    def disconnect(self):
        """
        socket通信を終了する関数

        Args:
            None

        Returns:
            None
        """

        self.connected = False
        try:
            self.client.close() # socket通信を終了
        except:
            print('fail to disconnect ' + self.hostname + '/' + str(self.port))

    def send(self, cmd):
        """
        サーバにコマンドを送信する関数

        Args:
            cmd (str): 送信したいコマンド

        Returns:
            None
        """
        cmd += '\n' # フッターが'\n'なので送信コマンドの最後に'\n'をつける

        try:
            self.client.send(cmd.encode('utf-8')) # '送信コマンドをUTF-8にエンコードし, サーバへ送信'
        except:
            self.connected = False
            print('fail to send message -> ' + cmd)


    def receive(self):
        """
        サーバからの送られてきたデータを受信する関数

        Args:
            None

        Returns:
            entire_msg (str): 受信したデータ
        """
        entire_msg = '' # 受信したデータを格納する変数

        self.client.settimeout(0.01) # タイムアウトを設定

        # フッター'\n'を受信するまで無限ループ
        while True:
            try:
                recv_msg = self.client.recv(8192).decode('utf-8') # データを受信, デコード
                entire_msg += recv_msg # 一回の受信では全データ受信できない可能性があるため, 一つの変数にデータをためておく
                if '\n' in recv_msg:
                    break

            # データ受信時に設定されたタイムアウトを超えたら例外発生 (何もしないで関数から抜ける)
            except socket.timeout:
                return None

        return entire_msg

    def read_json_object(self):
        """
        サーバからの送られてきたJSONデータを受信する関数

        Args:
            None

        Returns:
            json_obj (str): 受信したJSONデータ
        """
        entire_msg = '' # 受信したデータを格納する変数
        json_obj = '' # JSONデータを格納する変数

        self.client.settimeout(0.01) # タイムアウトを設定 (10ms)

        while True:
            try:
                recv_msg = self.client.recv(1024).decode('utf-8') # データを受信, デコード
                entire_msg += recv_msg # 一つの変数にデータをためておく

                # '{"topic"'という文字列で始まり, '}{'で終わるような正規表現パターンを検索
                search_pattern = re.search(r'\{\"topic\".*\}\{', entire_msg)

                # そのパターンが存在するとき, 該当部分の文字列を取得し, ループから抜ける
                if search_pattern:
                    start_pos = search_pattern.start() # 正規表現パターンの開始位置取得
                    end_pos = search_pattern.end() # 正規表現パターンの終了位置取得
                    json_obj = entire_msg[start_pos:end_pos-1] # 全データから該当部分をスライスで取得 (end_pos-1にした理由は最後が'}{'となるため)
                    break

            # データ受信時に設定されたタイムアウトを超えたら例外発生 (何もしないで関数から抜ける)
            except socket.timeout:
                return None

        return json_obj