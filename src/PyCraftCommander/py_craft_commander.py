from PyCraftCommander.rcon import RCON


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
