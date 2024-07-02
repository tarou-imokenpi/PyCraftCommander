from rcon import RCON

host = "localhost"
port = 25575

with RCON("localhost", "25575", "admin") as r:
    r.auth()
    r.command("say Hello, World!")
