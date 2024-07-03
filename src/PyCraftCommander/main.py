from PyCraftCommander import PyCraftCommander

host = "localhost"
port = 25575
password = "admin"

with PyCraftCommander(host, port, password) as server:
    server.auth()

    player_list, _ = server.get_player_list()
    # if status:
    #     print("リクエスト成功")
    print(f"プレイヤーリスト:{player_list}")
