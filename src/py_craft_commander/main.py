from py_craft_commander import PyCraftCommander

host = "localhost"
port = 25575
password = "admin"

with PyCraftCommander(host, port, password) as server:
    server.auth()

    body, status = server.send_command("say Hello, World!")
    if not status:
        print("正しいレスポンスIDが返ってきませんでした。")
        exit(1)

    print("リクエスト成功！")
    print(f"応答:{body}")
