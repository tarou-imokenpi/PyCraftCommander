from PyCraftCommander.rcon import RCON
from PyCraftCommander.types.player import Player, Pos


class PyCraftCommander(RCON):
    def __init__(self, host, port, password):
        super().__init__(host, port, password)

    def get_player_list(self) -> list[str]:
        """マインクラフトサーバーのプレイヤーリストを取得します。

        Returns:
        -------
            list[str]: プレイヤーリスト
        """
        response, status = self.send_command("list")
        if not status:
            return []
        return response.split(": ")[1].split(", ")

    def get_player_info(self, player: str) -> Player:
        """プレイヤーの情報を取得します。

        Args:
        -----
            player (str): プレイヤー名

        Returns:
        -------
            Player: プレイヤーオブジェクト

        Example:
        --------
        ```python
        p = server.get_player_info("player_name")

        print(f"プレイヤー名:{p.name}")
        print(f"座標:{p.pos}")
        print(f"X:{p.pos.x}")
        print(f"Y:{p.pos.y}")
        print(f"Z:{p.pos.z}")
        print(f"ディメンション:{p.dimension}")
        print(f"ゲームモード:{p.gamemode}")
        ```
        """
        response, status = self.send_command(f"data get entity {player} Pos")
        if not status:
            return None
        pos = response.split(": ")[-1]
        pos = pos.translate(str.maketrans("", "", "[]")).split(", ")

        x, y, z = float(pos[0][:-1]), float(pos[1][:-1]), float(pos[2][:-1])

        response, status = self.send_command(f"data get entity {player} Dimension")
        if not status:
            return None
        dimension = response.split(" ")[-1]

        response, status = self.send_command(f"data get entity {player} playerGameType")
        if not status:
            return None
        gamemode = response.split(" ")[-1]

        return Player(player, Pos(x, y, z), dimension, gamemode)

    def tp(self, from_: str, to: str) -> str:
        """プレイヤーをテレポートします。

        Args:
        -----
            from_ (str): 移動させるプレイヤー
            to (str): 移動先のプレイヤー

        return:
        ------
            str: レスポンスメッセージ
        """
        if from_ == to and (from_ not in "@" or to not in "@"):
            return "同じプレイヤーにはテレポートできません。"

        response, status = self.send_command(f"tp {from_} {to}")
        return response
