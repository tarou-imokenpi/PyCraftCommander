from dataclasses import dataclass
from enum import IntEnum


@dataclass
class Packet:
    """RCONパケットのデータ構造を定義するデータクラス

    Attributes:
    ----------
    size: パケットのサイズ
    request_id: リクエストID
    type: パケットタイプ
    body: パケットの本文
    empty_string: 終端文字
    """

    size: int
    request_id: int
    type: int
    body: str
    empty_string: bytes = b"\x00\x00"


class PacketType(IntEnum):
    """4バイトのパケットタイプを定義する列挙型"""

    SERVERDATA_AUTH = 3
    SERVERDATA_AUTH_RESPONSE = 2
    SERVERDATA_EXECCOMMAND = 2
    SERVERDATA_RESPONSE_VALUE = 0
