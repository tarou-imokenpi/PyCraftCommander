from PyCraftCommander.rcon import RCON
from PyCraftCommander.types.player import Player, Pos, GameMode
from typing import Literal


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
        return sorted(response.split(": ")[1].split(", "))

    def get_player_info(self, player_name: str) -> Player:
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
        response, status = self.send_command(f"data get entity {player_name} Pos")
        if not status:
            return None
        pos = response.split(": ")[-1]
        pos = pos.translate(str.maketrans("", "", "[]")).split(", ")

        x, y, z = float(pos[0][:-1]), float(pos[1][:-1]), float(pos[2][:-1])

        response, status = self.send_command(f"data get entity {player_name} Dimension")
        if not status:
            return None
        dimension = response.split(" ")[-1]

        response, status = self.send_command(
            f"data get entity {player_name} playerGameType"
        )
        if not status:
            return None
        gamemode = response.split(" ")[-1]

        return Player(
            player_name, Pos(x, y, z), Pos(int(x), int(y), int(z)), dimension, gamemode
        )

    def tp(self, from_: str | Player, to: str | Player) -> str:
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
        if isinstance(from_, Player):
            from_ = from_.name
        if isinstance(to, Player):
            to = to.name

        response, status = self.send_command(f"tp {from_} {to}")
        return response

    def set_block(
        self,
        pos: Player | Pos | str,
        block_id: str,
        mode: Literal["replace", "keep", "destroy"] = "replace",
    ) -> str:
        """ブロックを設置します。

        Args:
        -----
            pos (Player | Pos | str): ブロックを設置する座標
            block_id (str): ブロックID

        Returns:
        -------
            str: レスポンスメッセージ
        """
        if isinstance(pos, Player):
            pos = pos.int_pos

        response, status = self.send_command(f"setblock {pos} {block_id} {mode}")
        return response

    def fill(
        self,
        pos1: Player | Pos | str,
        pos2: Player | Pos | str,
        block_id: str,
        mode: Literal["replace", "keep", "destroy", "hollow", "outline"] = "replace",
    ) -> str:
        """範囲内にブロックを設置します。

        Args:
        -----
            pos1 (Player | Pos | str): 範囲の座標1
            pos2 (Player | Pos | str): 範囲の座標2
            block_id: ブロックID
            mode: モード

        Returns:
        -------
            str: レスポンスメッセージ
        """
        if isinstance(pos1, Player):
            pos1 = pos1.pos
        if isinstance(pos2, Player):
            pos2 = pos2.pos

        response, status = self.send_command(f"fill {pos1} {pos2} {block_id} {mode}")
        return response

    def gamemode(
        self,
        mode: (
            GameMode | Literal["survival", "creative", "adventure", "spectator"] | int
        ),
        target: str | Player,
    ) -> str:
        """ゲームモードを変更します。

        Args:
        -----
            mode (str | int): ゲームモード
            target (str | Player): 対象プレイヤー

        Returns:
        -------
            str: レスポンスメッセージ
        """
        if isinstance(target, Player):
            target = target.name

        response, status = self.send_command(f"gamemode {mode} {target}")
        return response

    def give(self, target: str | Player, item: str, count: int = 1) -> str:
        """アイテムを付与します。

        Args:
        -----
            target (str | Player): 対象プレイヤー
            item (str): アイテムID
            count (int): 個数

        Returns:
        -------
            str: レスポンスメッセージ
        """
        if isinstance(target, Player):
            target = target.name

        response, status = self.send_command(f"give {target} {item} {count}")
        return response

    def clear(self, target: str | Player, item: str = "") -> str:
        """アイテムをクリアします。

        Args:
        -----
            target (str | Player): 対象プレイヤー
            item (str): アイテムID

        Returns:
        -------
            str: レスポンスメッセージ
        """
        if isinstance(target, Player):
            target = target.name

        response, status = self.send_command(f"clear {target} {item}")
        return response

    def difficulty(
        self, difficulty: Literal["peaceful", "easy", "normal", "hard"] | int
    ) -> str:
        """難易度を変更します。

        Args:
        -----
            difficulty (str): 難易度

        Returns:
        -------
            str: レスポンスメッセージ
        """
        response, status = self.send_command(f"difficulty {difficulty}")
        return response

    def effect_clear(self, target: str | Player, effect: str) -> str:
        """エフェクトをクリアします。

        Args:
        -----
            target (str | Player): 対象プレイヤー

        Returns:
        -------
            str: レスポンスメッセージ
        """
        if isinstance(target, Player):
            target = target.name

        response, status = self.send_command(f"effect clear {target} {effect}")
        return response

    def effect_give(
        self,
        target: str | Player,
        effect: str,
        seconds: int,
        lavel: int = 0,
        hideParticles: bool = False,
    ) -> str:
        """エフェクトを付与します。

        Args:
        -----
            target (str | Player): 対象プレイヤー
            effect (str): エフェクトID
            seconds (int): 持続時間(秒)
            lavel (int): レベル(0から255の値)
            hideParticles (bool): パーティクルを非表示にするか

        Returns:
        -------
            str: レスポンスメッセージ
        """
        if isinstance(target, Player):
            target = target.name

        response, status = self.send_command(
            f"effect give {target} {effect} {seconds} {lavel} {hideParticles}"
        )
        return response

    def effect_give_infinite(
        self,
        target: str | Player,
        effect: str,
        lavel: int = 0,
        hideParticles: bool = False,
    ) -> str:
        """エフェクトを無限に付与します。

        Args:
        -----
            target (str | Player): 対象プレイヤー
            effect (str): エフェクトID
            lavel (int): レベル(0から255の値)
            hideParticles (bool): パーティクルを非表示にするか

        Returns:
        -------
            str: レスポンスメッセージ
        """
        if isinstance(target, Player):
            target = target.name

        response, status = self.send_command(
            f"effect give {target} {effect} infinite {lavel} {hideParticles}"
        )
        return response
