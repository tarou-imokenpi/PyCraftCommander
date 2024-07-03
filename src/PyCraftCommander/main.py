from PyCraftCommander import PyCraftCommander

host = "localhost"
port = 25575
password = "admin"

with PyCraftCommander(host, port, password) as server:
    server.auth()

    player_list = server.get_player_list()
    # if status:
    #     print("リクエスト成功")
    print(f"プレイヤーリスト:{player_list}")

    print(server.send_command(f"data get entity {player_list[0]} Pos"))
