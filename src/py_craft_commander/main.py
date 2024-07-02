from py_craft_commander import PyCraftCommander

host = "localhost"
port = 25575
password = "admin"

with PyCraftCommander(host, port, password) as server:
    server.auth()

    player_list = server.get_player_list()

    print(f"プレイヤーリスト:{player_list}")
