from dataclasses import dataclass
from enum import IntEnum


@dataclass
class Pos:
    x: float
    y: float
    z: float

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"


class GameMode(IntEnum):
    SURVIVAL = 0
    CREATIVE = 1
    ADVENTURE = 2
    SPECTATOR = 3


@dataclass
class Player:
    """プレイヤー情報を格納するデータクラス

    Attributes:
    ----------
    name: プレイヤー名
    Pos: プレイヤーの座標(x,y,z)
    dimension: プレイヤーのディメンション
    gamemode: ゲームモード
    """

    name: str
    pos: Pos
    dimension: str
    gamemode: GameMode | str
