import socket
import struct
import random
from enum import IntEnum
from dataclasses import dataclass


class PacketType(IntEnum):
    """4バイトのパケットタイプを定義する列挙型"""

    SERVERDATA_AUTH = 3
    SERVERDATA_AUTH_RESPONSE = 2
    SERVERDATA_EXECCOMMAND = 2
    SERVERDATA_RESPONSE_VALUE = 0


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


class RCONClient:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password

    def row_data_send(self, command):
        with RCON(self.host, self.port, self.password) as rcon:
            return rcon.command(command)


class RCON:
    """RCONプロトコルを用いてMinecraftサーバーにコマンドを送信するためのクラス"""

    # 4バイトの符号付き整数フォーマット
    i32 = struct.Struct("<i")
    # responseパケットの構造
    res_struct = struct.Struct("<iii")

    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((self.host, int(self.port)))
            self.socket.settimeout(5.0)
        except ConnectionRefusedError:
            raise ConnectionRefusedError(
                "サーバーに接続できませんでした。\nサーバが起動していてホスト名とポート番号が正しいか確認してください。"
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.socket.close()

    def __del__(self):
        self.socket.close()

    def auth(self):
        """RCON認証を行います。"""
        response_id = self.send_packet(PacketType.SERVERDATA_AUTH, self.password)
        return self.auth_response(response_id)

    def auth_response(self, request_id: int):
        """RCON認証のレスポンスを受信します。"""
        packet: Packet = self.receive_packet()
        if (
            packet.request_id == request_id
            and packet.type == PacketType.SERVERDATA_AUTH_RESPONSE
        ):
            return True

        raise Exception("RCON認証に失敗しました。\nパスワードが間違っているようです。")

    def server_response_value(self):
        """サーバーからのレスポンスを受信します。"""
        response = self.receive_packet()
        print(f"Packet Size: {response.size}")
        print(f"Request ID: {response.request_id}")
        print(f"Type: {response.type}")
        print(f"Body: {response.body}")

    def command(self, command):
        """マインクラフトサーバーにコマンドを送信します。"""
        request_id = self.send_packet(PacketType.SERVERDATA_EXECCOMMAND, command)
        return self.server_response_value()

    def send_packet(self, type: int, body: str) -> bytes:
        """パケットを送信し、リクエストIDを返します。"""
        # パケットのサイズは、12バイトのヘッダーと2バイトの終端文字を含む
        # リトルエンディアンでパックする
        # size | ID | Type | Body + Null | Null
        # 4    | 4  | 4    | size + 1    | 1

        body: bytes = body.encode("utf-8")
        type: bytes = self.i32.pack(int(type))

        packet_size: bytes = self.i32.pack(len(body) + 10)

        # ランダムなパケットIDを生成(4バイトの符号付き整数) 2147483647
        ramdom_id = random.randint(0, 2147483647)
        request_id: bytes = self.i32.pack(ramdom_id)

        packet: bytes = packet_size + request_id + type + body + b"\x00\x00"
        self.socket.sendall(packet)
        return ramdom_id

    def receive_packet(self) -> Packet:
        """パケットを受信し、Packetを返します"""
        respone = self.socket.recv(4096)
        size, request_id, type = self.res_struct.unpack(respone[:12])
        body = respone[12:-2]
        return Packet(size, request_id, type, body)
