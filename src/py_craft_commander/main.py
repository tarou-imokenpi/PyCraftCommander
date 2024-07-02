from rcon import RCON

host = "localhost"
port = 25575
password = "admin"

with RCON(host, port, password) as r:
    r.auth()
    r.command("say Hello, World!")
