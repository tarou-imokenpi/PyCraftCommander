from rcon import RCON


class PyCraftCommander(RCON):
    def __init__(self, host, port, password):
        super().__init__(host, port, password)

    def get_player_list(self):
        """マインクラフトサーバーのプレイヤーリストを取得します。"""
        return self.send_command("list")
