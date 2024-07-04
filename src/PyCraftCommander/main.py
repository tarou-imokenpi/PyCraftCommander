from PyCraftCommander import PyCraftCommander, Player, GET_MCID
import random
import time
from copy import deepcopy

host = "localhost"
port = 25575
password = "admin"

with PyCraftCommander(host, port, password) as server:
    MCID = GET_MCID("1.21")
    server.auth()

    player_list = server.get_player_list()
    print(f"プレイヤーリスト:{player_list}")

    p: Player = server.get_player_info(player_list[0])

    print(f"プレイヤー名:{p.name}")
    print(f"座標:{p.pos}")
    print(f"ディメンション:{p.dimension}")
    print(f"ゲームモード:{p.gamemode}")

    num = 10

    block = MCID.GOLD_BLOCK

    area = deepcopy(p.int_pos)

    pos1 = area
    pos2 = area
    pos2.x += num
    pos2.y += num
    res = server.fill(pos1, pos2, block)

    print(res)
