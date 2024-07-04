from PyCraftCommander import PyCraftCommander, Player, GET_MCID
import random
import time

host = "10.0.68.31"
port = 25575
password = "taro"

with PyCraftCommander(host, port, password) as server:
    MCID = GET_MCID("1.21")
    server.auth()

    player_list = server.get_player_list()
    print(f"プレイヤーリスト:{player_list}")

    p: Player = server.get_player_info(player_list[0])

    print(f"プレイヤー名:{p.name}")
    print(f"座標:{p.pos}")
    print(f"X:{p.pos.x}")
    print(f"Y:{p.pos.y}")
    print(f"Z:{p.pos.z}")
    print(f"ディメンション:{p.dimension}")
    print(f"ゲームモード:{p.gamemode}")

    # server.send_command(f"give @a {MCID.ACACIA_BUTTON}")
    for i in range(10):
        server.send_command(f"setblock {p.pos.x} {p.pos.y} {p.pos.z} {MCID.ACACIA_LOG}")
        time.sleep(0.5)
