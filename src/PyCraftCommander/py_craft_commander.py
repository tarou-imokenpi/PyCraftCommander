from PyCraftCommander.rcon import RCON
from typing import Literal


class PyCraftCommander(RCON):
    TARGET = Literal["@a", "@r", "@e", "@p"]

    def __init__(self, host, port, password):
        super().__init__(host, port, password)

    def get_player_list(self) -> list[str]:
        """マインクラフトサーバーのプレイヤーリストを取得します。"""
        response, status = self.send_command("list")
        if not status:
            return []
        return response.split(": ")[1].split(", ")

    def tp(self, from_: TARGET | str, to: TARGET | str) -> str:
        """プレイヤーをテレポートします。"""
        if from_ == to and from_ not in self.TARGET:
            return "同じプレイヤーにはテレポートできません。", False

        response, status = self.send_command(f"tp {from_} {to}")
        return response
