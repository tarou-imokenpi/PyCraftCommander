import socket
import struct
import random
from enum import IntEnum


class RCONClient:
    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password

    def row_data_send(self, command):
        with RCON(self.host, self.port, self.password) as rcon:
            return rcon.command(command)


class RCON:
    # パケットの終端文字
    end_packet: bytes = b"x00x00"

    def __init__(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

    def command(self, command):
        self.send_packet(3, command)
        return self.receive_packet()

    def send_packet(self, type, body):
        # パケットのサイズは、12バイトのヘッダーと2バイトの終端文字を含む
        # リトルエンディアンでパックする
        # size | ID | Type | Body + Null | Null
        # 4    | 4  | 4    | size        |

        body: bytes = body.encode("utf-8")
        packet_size = struct.pack("<iii", len(body) + 10)

        # ランダムなパケットIDを生成(4バイトの符号付き整数)
        id = struct.pack("<i", random.randint(0, 2147483647))

        packet: bytes = packet_size + id + type + body + self.end_packet
        self.socket.sendall(packet)

    def receive_packet(self):
        size, request_id, type = struct.unpack("<iii", self.socket.recv(12))
        if type == -1:
            error = self.socket.recv(size - 8)
            raise Exception(f'RCON Error: {error.decode("utf-8")}')
        return self.socket.recv(size - 8).decode("utf-8")


class PacketType(IntEnum):
    """4バイトのパケットタイプを定義する列挙型"""

    SERVERDATA_AUTH = 3
    SERVERDATA_AUTH_RESPONSE = 2
    SERVERDATA_EXECCOMMAND = 2
    SERVERDATA_RESPONSE_VALUE = 0
