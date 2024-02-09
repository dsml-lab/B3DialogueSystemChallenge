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
# from communicator import Communicator # 親クラス
# コンソールで実行するときは以下のimport文をアンコメント
# from communicator import Communicator

class RobotBodyController(Communicator):
    """
    ロボットの動作制御クラス

    Args:
        hostname (str): ホスト名
        port (int): ポート番号
    """
    def __init__(self, hostname, port):
        # 与えられたホスト名, ポート名でSocket通信のクライアントを作成
        super().__init__(hostname, port)


    def play_motion(self, motion_id):
        cmd = 'playmotion=' + motion_id
        self.client.send(cmd)
        self.set_tracking()


    def set_gaze(self, x, y, z):
        """
        x, y, zで視線や頭の向きを制御するクラス

        Args:
            x (int): x軸方向の視線や頭の向き
            y (int): y軸報告の視線や頭の向き
            z (int): z軸方向の視線や頭の向き

        Returns:
            None
        """
        cmd = self.create_gaze_command('EyeController', '', x, y, z)
        self.client.send(cmd)
        cmd = self.create_gaze_command('HeadController', '', x, y, z)
        self.client.send(cmd)


    def set_gaze_to_object(self, object_name):
        """
        視線や頭を向けたいオブジェクト名を入力することで制御するクラス

        Args:
            object_name

        Returns:
            None
        """
        cmd = self.create_gaze_command('EyeController', object_name, 0, 0, 0) # 送信コマンドを作成 (視線)
        self.client.send(cmd) # サーバにコマンドを送信
        cmd = self.create_gaze_command('HeadController', object_name, 0, 0, 0) # 送信コマンドを作成 (頭)
        self.client.send(cmd) # サーバにコマンドを送信


    def create_gaze_command(self, controller_name, object_name, x, y, z):
        """
        与えられた引数でJSON形式のコマンドを作成するクラス

        Args:
            controller_name (str): 視線, 頭, 体のどれを動かすか
            object_name (str): どこを見るかをobjectで指定
            x (int): x軸方向の視線や頭の向き
            y (int): y軸報告の視線や頭の向き
            z (int): z軸方向の視線や頭の向き

        Returns:
            cmd (str): 送信コマンド
        """
        point = dict()
        cmd = dict()
        point['x'] = x
        point['y'] = y
        point['z'] = z

        cmd['id'] = controller_name
        cmd['motionTowardObject'] = object_name
        cmd['tracking'] = True # ユーザの視線追尾の有無
        cmd['targetMotionMode'] = 2
        cmd['targetPoint'] = point
        cmd['translateSpeed'] = 2.0

        cmd = json.dumps(cmd)
        cmd = controller_name + '=' + cmd
        return cmd

    # def create_tracking_command(self, controller_name, object_name):
    def create_tracking_command(self, name):
        cmd = dict()
        
        # cmd['id'] = controller_name
        # cmd['motionTowardObject'] = object_name
        # cmd['tracking'] = True # ユーザの視線追尾の有無

        # cmd = json.dumps(cmd)
        # cmd = controller_name + '=' + cmd
        if name == 'HeadController':
            cmd['id'] = name
            cmd['motionTowardObject'] = 'humanhead'
            cmd['targetMotionMode'] = 2
            cmd['targetPoint'] = {'x': 0, 'y': 0, 'z': 0}
            cmd['translateSpeed'] = 1.5
            cmd['translateTime'] = -1
            cmd['targetRotation'] = {'x': 0.0, 'y': 0.0, 'z': 0.0}
            cmd['rotateSpeed'] = 270
            cmd['rotateTime'] = -1
            cmd['keepTime'] = 0
            cmd['mode'] = 2
            cmd['gazeTracking'] = True
            cmd['tracking'] = True
            cmd['priority'] = 0
            cmd['isBezierCurvePoint'] = False
            cmd['finerData'] = []

            cmd = json.dumps(cmd)
            cmd = 'HeadController' + '=' + cmd
        elif name == 'EyeController':
            cmd['id'] = name
            cmd['motionTowardObject'] = 'humanhead'
            cmd['targetMotionMode'] = 2
            cmd['targetPoint'] = {'x': 0, 'y': 0, 'z': 0}
            cmd['translateSpeed'] = 2.0
            cmd['translateTime'] = -1
            cmd['targetRotation'] = {'x': 0.0, 'y': 0.0, 'z': 0.0}
            cmd['rotateSpeed'] = 270
            cmd['rotateTime'] = -1
            cmd['keepTime'] = 0
            cmd['mode'] = 2
            cmd['gazeTracking'] = True
            cmd['tracking'] = True
            cmd['priority'] = 0
            cmd['isBezierCurvePoint'] = False
            cmd['finerData'] = []

            cmd = json.dumps(cmd)
            cmd = 'EyeController' + '=' + cmd

        return cmd
    
    def set_tracking(self):
        cmd = dict()
        cmd = self.create_tracking_command('EyeController')
        self.client.send(cmd)
        cmd = self.create_tracking_command('HeadController')
        self.client.send(cmd)

    def create_tilt_command(self, controller_name, atractiveness):
        """
        与えられた引数でJSON形式のコマンドを作成するクラス

        Args:
            controller_name (str): 視線, 頭, 体のどれを動かすか
            object_name (str): どこを見るかをobjectで指定
            x (int): x軸方向の視線や頭の向き
            y (int): y軸報告の視線や頭の向き
            z (int): z軸方向の視線や頭の向き

        Returns:
            cmd (str): 送信コマンド
        """
        point = dict()
        cmd = dict()

        # cmd['id'] = controller_name
        cmd['atractiveness'] = atractiveness # -1.0~1.0

        cmd = json.dumps(cmd)
        cmd = controller_name + '=' + cmd
        return cmd  

    def send_cmd(self,cmd):
        self.client.send(cmd)

def main():
    #robot_body_controller = RobotBodyController('commuai.atr.jp', 21000)
    #robot_body_controller = RobotBodyController('133.14.214.124' , 21000)
    robot_body_controller = RobotBodyController('shoko-g-10' , 21000)
    robot_body_controller.start()
    # cmd = robot_body_controller.create_tilt_command("BodyController", 0.9)
    # robot_body_controller.send_cmd(cmd)
    # time.sleep(4)
    # cmd = robot_body_controller.create_gaze_command("BodyController", "", 0, 1.2, 1.5)
    # robot_body_controller.send_cmd(cmd)
    cmd = robot_body_controller.create_tracking_command('HeadController')
    robot_body_controller.send_cmd(cmd)
    cmd = robot_body_controller.create_tracking_command('EyeController')
    robot_body_controller.send_cmd(cmd)
    time.sleep(1)
    #robot_body_controller.play_motion('nod_slight')
    #time.sleep(4)
    #robot_body_controller.set_gaze( 0, 1.2, 1.5)

    robot_body_controller.stop()

if __name__=="__main__":
    main()