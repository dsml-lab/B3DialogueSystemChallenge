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

import time

from Module.communicator import Communicator # 親クラス
# # コンソールで実行するときは以下のimport文をアンコメント
# from communicator import Communicator

class RobotExpressionController(Communicator):
    """
    ロボットの表情制御クラス

    Args:
        hostname (str): ホスト名
        port (int): ポート番号
    """
    def __init__(self, hostname, port):
        # 与えられたホスト名, ポート名でSocket通信のクライアントを作成
        super().__init__(hostname, port)


    def set_expression(self, expression_preset_name):
        """
        表情制御するためのコマンドを送信する関数

        Args:
            expression_preset_name (str): 表情プリセット名
                                          fullsmile, angry, MoodBasedFACSを期待
                                          MoodBasedFACSは内部状態に応じて適宜変わる表情セット

        Returns:
            None
        """
        cmd = self.create_expression_command(expression_preset_name) # 送信コマンドを作成
        self.client.send(cmd) # コマンドを送信


    def create_expression_command(self, expression_preset_name):
        """
        送信コマンドを作成する関数

        Args:
            expression_preset_name (str): 表情プリセット名

        Returns:
            cmd (str): 送信コマンド "expression 表情プリセット名"のような形
        """
        cmd = 'expression ' + expression_preset_name
        return cmd

    def create_paramater(self, param_name, param_number):
        """
        送信コマンドを作成（パラメータ指定）

        Args:
            param_name (str): パラメータ名 'valence', 'arousal', 'dominance', 'realintention'のどれか
            param_number (float): 値 +1~-1

        Returns:
            cmd (str): 送信コマンド "パラメータ名 値"のような形
        """
        cmd = param_name + ' ' + str(param_number)
        return cmd

    def send_cmd(self,cmd):
        self.client.send(cmd)


# コンソール上で実行するときには以下が実行
if __name__ == '__main__':
    # ホスト名, ポート番号を指定し, オブジェクトを作成
    robot_expression_controller = RobotExpressionController('localhost', 20000)
    robot_expression_controller = RobotExpressionController('commuai.atr.jp', 20000)
    robot_expression_controller.start() # Socket通信を開始
    # robot_expression_controller.set_expression('fullsmile') # 表情プリセットをfullsmileに指定して, コマンドを送信
    # time.sleep(4) # 4秒間表情を固定
    # robot_expression_controller.set_expression('MoodBasedFACS') # 表情プリセットをMoodBasedFACSに指定して, コマンドを送信

    # robot_expression_controller.set_expression('angry') # 表情プリセットをfullsmileに指定して, コマンドを送信
    # time.sleep(4) # 4秒間表情を固定
    # robot_expression_controller.set_expression('MoodBasedFACS') # 表情プリセットをMoodBasedFACSに指定して, コマンドを送信
    cmd = robot_expression_controller.create_paramater('valence',0.2)
    robot_expression_controller.send_cmd(cmd)    
    cmd = robot_expression_controller.create_paramater('arousal',0.1)
    robot_expression_controller.send_cmd(cmd)
    cmd = robot_expression_controller.create_paramater('dominance',0)
    robot_expression_controller.send_cmd(cmd)
    cmd = robot_expression_controller.create_paramater('realintention',0)
    robot_expression_controller.send_cmd(cmd)
    time.sleep(4)
    cmd = robot_expression_controller.create_paramater('valence',0.2)
    robot_expression_controller.send_cmd(cmd)
    cmd = robot_expression_controller.create_paramater('arousal',0.1)
    robot_expression_controller.send_cmd(cmd)
    cmd = robot_expression_controller.create_paramater('dominance',0)
    robot_expression_controller.send_cmd(cmd)
    cmd = robot_expression_controller.create_paramater('realintention',0)
    robot_expression_controller.send_cmd(cmd)

    robot_expression_controller.stop() # Socket通信を終了