# PyCraftCommander

PyCraftCommander は、Minecraft Java Edition の RCON（Remote Console）を使ってサーバーを操作するための軽量な Python ライブラリです。`RCON` プロトコルをラップし、プレイヤー情報の取得、テレポート、ブロック配置、ゲームモード変更、アイテム付与、エフェクト付与など、よく使うコマンドを簡単に呼び出せる高水準な API を提供します。

> **💡 Tip**  
> 対象: Python 3.8 以上  
> 対応 Minecraft バージョン: 1.21 (mcid 列挙型に対応)

## 主な機能

- サーバーへ RCON 接続しコマンドを送信
- プレイヤー一覧、プレイヤー座標、ディメンション、ゲームモードの取得
- ブロック設置、範囲塗りつぶし (fill)
- テレポート、ゲームモード変更、アイテム付与/クリア
- エフェクトやエンチャント付与、kill、メッセージ送信など多数のユーティリティ
- Minecraft の ID を列挙した `GET_MCID()` ユーティリティ（v1.21 対応）

## インストール

ローカルからインストールする場合:

```bash
pip install .
```

GitHub から直接インストールする場合:

```bash
pip install git+https://github.com/tarou-imokenpi/PyCraftCommander.git
```

## セットアップ（RCON側）
Minecraft サーバーで RCON を有効にする必要があります。`server.properties` で下記を設定してください。

```ini
enable-rcon=true
rcon.port=25575
rcon.password=<your_password>
```

> **⚠️ Warning**  
> RCON パスワードは外部に漏れないように管理してください。RCON は強力な管理機能を持つため、公開サーバーではファイアウォールや ACL を使ってアクセス制限を行ってください。

## 使い方（Quickstart）

下記はライブラリ利用の基本的なサンプルです。

```python
from PyCraftCommander import PyCraftCommander, Player, GET_MCID

host = "localhost"
port = 25575
password = "your_password"

with PyCraftCommander(host, port, password) as server:
    server.auth()  # RCON 認証

    # プレイヤー一覧を取得
    players = server.get_player_list()
    print("Players:", players)

    # プレイヤー情報の取得
    if players:
        p: Player = server.get_player_info(players[0])
        print(p)

    # ブロック設置
    mcid = GET_MCID("1.21")
    server.set_block(p.int_pos, mcid.DIAMOND_BLOCK)

    # テレポート
    server.tp("PlayerA", "PlayerB")

    # チャットに送信
    server.say("Hello from PyCraftCommander!")
```

## API（主な関数）

- `PyCraftCommander(host, port, password)` — RCON 接続クラス
- `auth()` — RCON 認証を行う
- `get_player_list()` -> list[str]
- `get_player_info(player_name)` -> `Player`（`name`, `pos`, `int_pos`, `dimension`, `gamemode` を含む dataclass）
- `get_seed()` -> int
- `set_world_spawn(pos, angle=0.0)`
- `set_spawn_point(pos, angle=0.0)`
- `tp(from_, to)` — テレポート（プレイヤーまたはターゲット）
- `set_block(pos, block_id, mode='replace')`
- `fill(pos1, pos2, block_id, mode='replace')`
- `gamemode(mode, target)`
- `give(target, item, count=1)`
- `clear(target, item='')`
- `difficulty(level)`
- `effect_clear(target, effect)`
- `effect_give(target, effect, seconds, level=0, hideParticles=False)`
- `effect_give_infinite(target, effect, level=0, hideParticles=False)`
- `enchant(target, enchantment, level=1)`
- `kill(target)`
- `say(message)`
- `message(target, message)`

さらに、生データのやり取りが必要な場合は `send_command(command)` を使用して任意のコマンドを RCON 経由で送信できます。

## 型と補助ユーティリティ

- `Player` dataclass: `name`, `pos` (float), `int_pos` (int), `dimension`, `gamemode` などを持ちます。
- `Pos` dataclass: `x`, `y`, `z` を管理（文字列化されて `"x y z"` フォーマットが返されます）。
- `GET_MCID(version)` — Minecraft の名前空間付き ID を列挙した enum（現在対応: `"1.21"`）。

## 例: ダイヤモンドブロックでオブジェクトを作る

### 例1: 下に垂直に 10 ブロック配置

```python
from PyCraftCommander import PyCraftCommander, GET_MCID, Pos
import time

host = 'localhost'
port = 25575
password = 'password'

with PyCraftCommander(host, port, password) as server:
    server.auth()
    players = server.get_player_list()
    if players:
        p = server.get_player_info(players[0])
        mcid = GET_MCID('1.21')

        # プレイヤーの下 10 ブロックに垂直にダイヤモンドを配置
        start_y = int(p.pos.y) - 1  # プレイヤーの 1 ブロック下
        for i in range(10):
            pos = Pos(int(p.pos.x), start_y - i, int(p.pos.z))
            server.set_block(pos, mcid.DIAMOND_BLOCK)
            time.sleep(0.01)
```

### 例2: 正方形グリッド（10×10）を描く

```python
from PyCraftCommander import PyCraftCommander, GET_MCID, Pos
import time

host = 'localhost'
port = 25575
password = 'password'

with PyCraftCommander(host, port, password) as server:
    server.auth()
    players = server.get_player_list()
    if players:
        p = server.get_player_info(players[0])
        mcid = GET_MCID('1.21')

        # プレイヤーの下 10 ブロック地点から xy 平面に 10×10 の正方形を描く
        base_x = int(p.pos.x)
        base_y = int(p.pos.y) - 1
        base_z = int(p.pos.z)

        for x_offset in range(10):
            for z_offset in range(10):
                pos = Pos(base_x + x_offset, base_y, base_z + z_offset)
                server.set_block(pos, mcid.DIAMOND_BLOCK)
                time.sleep(0.01)
```

## 注意点

- ライブラリは RCON を直接利用するため、送信するコマンドやレスポンスは Minecraft のコンソールの挙動に依存します。
- RCON はサーバー管理向けの機能です。誤ったコマンドはワールド破損やプレイヤーのデータ消失など重大な影響を与える可能性があるので注意して使用してください。

## バージョンと互換性

- Python 3.8 以上をサポートします。
- `GET_MCID` は `"1.21"` をサポートしています。別バージョンを使う場合は `GET_MCID()` または mcid enum を拡張してください。