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

    block = MCID.DIAMOND_BLOCK

    myPos = deepcopy(p.int_pos)
    myPos.x += 0
    myPos.y -= 10
    myPos.z += 0

    time.sleep(1)
    count = 0
    for i in range(10):
        # myPos.x -= 1s

        for i in range(10):
            myPos.x += 1
            server.set_block(myPos, block)
            time.sleep(0.01)

        for i in range(10):
            myPos.z += 1
            server.set_block(myPos, block)
            time.sleep(0.01)

        for i in range(10):

            server.set_block(myPos, block)
            time.sleep(0.01)

        for i in range(10):
            server.set_block(myPos, block)
            time.sleep(0.01)

        myPos.y += 1
        myPos.z -= 1
        count += 1
