import socket
import struct
import random
from PyCraftCommander.types.packet import Packet, PacketType


class RCON:
    """RCONプロトコルを用いてMinecraftサーバーにコマンドを送信するためのクラス"""

    # 4バイトの符号付き整数フォーマット
    __i32 = struct.Struct("<i")
    # responseパケットの構造
    __res_struct = struct.Struct("<iii")

    def __init__(self, host, port, password):
        self.__host = host
        self.__port = port
        self.__password = password
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.__socket.connect((self.__host, int(self.__port)))
            self.__socket.settimeout(5.0)
        except ConnectionRefusedError:
            raise ConnectionRefusedError(
                "サーバーに接続できませんでした。\nサーバが起動していてホスト名とポート番号が正しいか確認してください。"
            )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.__socket.close()

    def __del__(self):
        self.__socket.close()

    def auth(self):
        """RCON認証を行います。"""
        response_id = self.send_packet(PacketType.SERVERDATA_AUTH, self.__password)
        return self.__auth_response(response_id)

    def __auth_response(self, request_id: int):
        """RCON認証のレスポンスを受信します。"""
        packet: Packet = self.receive_packet()
        if (
            packet.request_id == request_id
            and packet.type == PacketType.SERVERDATA_AUTH_RESPONSE
        ):
            return True

        raise Exception("RCON認証に失敗しました。\nパスワードが間違っているようです。")

    def server_response_value(self, request_id: int):
        """サーバーからのレスポンスを受信します。"""
        packet: Packet = self.receive_packet()
        # -----------------------------------
        # debug only
        # print(f"Packet Size: {packet.size}")
        # print(f"Request ID: {packet.request_id}")
        # print(f"Type: {packet.type}")
        # print(f"Body: {packet.body}")
        # -----------------------------------
        if packet.request_id == request_id:
            return (packet.body.decode("utf-8"), True)
        return ("", False)

    def send_command(self, command) -> tuple[str, bool]:
        """マインクラフトサーバーにコマンドを送信します。"""
        request_id = self.send_packet(PacketType.SERVERDATA_EXECCOMMAND, command)
        return self.server_response_value(request_id)

    def send_packet(self, type: int, body: str) -> bytes:
        """パケットを送信し、リクエストIDを返します。"""
        # パケットのサイズは、12バイトのヘッダーと2バイトの終端文字を含む
        # リトルエンディアンでパックする
        # size | ID | Type | Body + Null | Null
        # 4    | 4  | 4    | size + 1    | 1

        body: bytes = body.encode("utf-8")
        type: bytes = self.__i32.pack(int(type))

        packet_size: bytes = self.__i32.pack(len(body) + 10)

        # ランダムなパケットIDを生成(4バイトの符号付き整数) 2147483647
        ramdom_id = random.randint(0, 2147483647)
        request_id: bytes = self.__i32.pack(ramdom_id)

        packet: bytes = packet_size + request_id + type + body + b"\x00\x00"
        self.__socket.sendall(packet)
        return ramdom_id

    def receive_packet(self) -> Packet:
        """パケットを受信し、Packetを返します"""
        respone = self.__socket.recv(4096)
        size, request_id, type = self.__res_struct.unpack(respone[:12])
        body = respone[12:-2]
        return Packet(size, request_id, type, body)
