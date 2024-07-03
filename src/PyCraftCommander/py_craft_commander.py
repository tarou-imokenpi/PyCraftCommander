from PyCraftCommander.rcon import RCON


class PyCraftCommander(RCON):
    def __init__(self, host, port, password):
        super().__init__(host, port, password)

    def get_player_list(self) -> list[str]:
        """マインクラフトサーバーのプレイヤーリストを取得します。"""
        response, status = self.send_command("list")
        if not status:
            return []
        return response.split(": ")[1].split(", ")
