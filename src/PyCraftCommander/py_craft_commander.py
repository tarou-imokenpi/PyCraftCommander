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
        level: int = 0,
        hideParticles: bool = False,
    ) -> str:
        """エフェクトを付与します。

        Args:
        -----
            target (str | Player): 対象プレイヤー
            effect (str): エフェクトID
            seconds (int): 持続時間(秒)
            level (int): レベル(0から255の値)
            hideParticles (bool): パーティクルを非表示にするか

        Returns:
        -------
            str: レスポンスメッセージ
        """
        if isinstance(target, Player):
            target = target.name

        response, status = self.send_command(
            f"effect give {target} {effect} {seconds} {level} {hideParticles}"
        )
        return response

    def effect_give_infinite(
        self,
        target: str | Player,
        effect: str,
        level: int = 0,
        hideParticles: bool = False,
    ) -> str:
        """エフェクトを無限に付与します。

        Args:
        -----
            target (str | Player): 対象プレイヤー
            effect (str): エフェクトID
            level (int): レベル(0から255の値)
            hideParticles (bool): パーティクルを非表示にするか

        Returns:
        -------
            str: レスポンスメッセージ
        """
        if isinstance(target, Player):
            target = target.name

        response, status = self.send_command(
            f"effect give {target} {effect} infinite {level} {hideParticles}"
        )
        return response

    def enchant(self, target: str | Player, enchantment: str, level: int = 1) -> str:
        """エンチャントを付与します。

        Args:
        -----
            target (str | Player): 対象プレイヤー
            enchantment (str): エンチャントID
            level (int): そのエンチャントで可能な最大レベルまで指定可能

        Returns:
        -------
            str: レスポンスメッセージ
        """
        if isinstance(target, Player):
            target = target.name

        response, status = self.send_command(f"enchant {target} {enchantment} {level}")
        return response

    def kill(self, target: str | Player) -> str:
        """プレイヤーを殺します。

        Args:
        -----
            target (str | Player): 対象プレイヤー

        Returns:
        -------
            str: レスポンスメッセージ
        """
        if isinstance(target, Player):
            target = target.name

        response, status = self.send_command(f"kill {target}")
        return response

    def forceload_add(
        self,
        posA: str,
        posB: str = None,
        orver_world: bool = True,
        the_nether: bool = False,
        the_end: bool = False,
    ) -> str:
        """チャンクを強制ロードします。

        チャンクの座標ではなくブロックの座標を指定する必要があります。
        座標は、XとZの値をカンマで区切って指定します。

        注意:
        * 作物の成長などランダムティックを使用するものは強制読み込みに加えチャンクの128ブロック以内の範囲にいないと機能しません。

        Args:
        -----
            posA (str): <posA>の常時読み込みを強制する。
            posB (str): <posB>を指定すると範囲を指定して、範囲全体を常時読み込みさせることができる。デフォルトはNone。
            orver_world (bool): オーバーワールドを強制読み込みに追加するか。デフォルトはTrue。
            the_nether (bool): ネザーを強制読み込みに追加するか。デフォルトはFalse。
            the_end (bool): エンドを強制読み込みに追加するか。デフォルトはFalse。

        Returns:
        -------
            str: レスポンスメッセージ
        """

        command = f"forceload add {posA}"
        if posB:
            command += f" {posB}"
        if orver_world:
            result, status = self.send_command(command) + "\n"
        if the_nether:
            result, status += self.send_command(f"execute in minecraft:the_nether run {command}") + "\n"
        if the_end:
            result, status += self.send_command(f"execute in minecraft:the_end run {command}") + "\n"
        return result[:-1]

    def forceload_remove(
        self,
        posA: str,
        posB: str = None,
        orver_world: bool = True,
        the_nether: bool = False,
        the_end: bool = False,
    ) -> str:
        """強制ロードを解除します。

        チャンクの座標ではなくブロックの座標を指定する必要があります。
        座標は、XとZの値をカンマで区切って指定します。

        Args:
        -----
            posA (str): <posA>の常時読み込みを解除する。
            posB (str): <posB>を指定すると範囲を指定して、範囲全体の常時読み込みを解除することができる。デフォルトはNone。
            orver_world (bool): オーバーワールドの強制読み込みを解除するか。デフォルトはTrue。
            the_nether (bool): ネザーの強制読み込みを解除するか。デフォルトはFalse。
            the_end (bool): エンドの強制読み込みを解除するか。デフォルトはFalse。

        Returns:
        -------
            str: レスポンスメッセージ
        """

        command = f"forceload remove {posA}"
        if posB:
            command += f" {posB}"
        if orver_world:
            result, status = self.send_command(command) + "\n"
        if the_nether:
            result, status += self.send_command(f"execute in minecraft:the_nether run {command}") + "\n"
        if the_end:
            result, status += self.send_command(f"execute in minecraft:the_end run {command}") + "\n"
        return result[:-1]

    def forceload_remove_all(self, orver_world: bool = True, the_nether: bool = False, the_end: bool = False) -> str:
        """全ての強制ロードを解除します。

        Args:
        -----
            orver_world (bool): オーバーワールドの強制読み込みを解除するか。デフォルトはTrue。
            the_nether (bool): ネザーの強制読み込みを解除するか。デフォルトはFalse。
            the_end (bool): エンドの強制読み込みを解除するか。デフォルトはFalse。

        Returns:
        -------
            str: レスポンスメッセージ
        """

        command = "forceload remove all"
        if orver_world:
            result, status = self.send_command(command) + "\n"
        if the_nether:
            result, status += self.send_command(f"execute in minecraft:the_nether run {command}") + "\n"
        if the_end:
            result, status += self.send_command(f"execute in minecraft:the_end run {command}") + "\n"
        return result[:-1]

    def forceload_query(self, pos: str=None, orver_world: bool = True, the_nether: bool = False, the_end: bool = False) -> str:
        """強制ロードの状態を確認します。引数がない場合はorver_worldの強制ロードの状態を確認します。

        チャンクの座標ではなくブロックの座標を指定する必要があります。
        座標は、XとZの値をカンマで区切って指定します。

        Args:
        -----
            pos (str): 状態を確認する座標
            orver_world (bool): オーバーワールドの状態を確認するか。デフォルトはTrue。
            the_nether (bool): ネザーの状態を確認するか。デフォルトはFalse。
            the_end (bool): エンドの状態を確認するか。デフォルトはFalse。

        Returns:
        -------
            str: レスポンスメッセージ
        """

        command = f"forceload query"
        if pos:
            command += f" {pos}"
        if orver_world:
            result, status = self.send_command(command) + "\n"
        if the_nether:
            result, status += self.send_command(f"execute in minecraft:the_nether run {command}") + "\n"
        if the_end:
            result, status += self.send_command(f"execute in minecraft:the_end run {command}") + "\n"
        return result[:-1]