import asyncio
import json
import websockets
import requests
from colorama import Fore, Style
from random import randint
from time import sleep

def split_chunk(var):
    if isinstance(var, int):
        var = str(var)
    n = 3
    var = var[::-1]
    return ' '.join([var[i:i + n] for i in range(0, len(var), n)])[::-1]

class Battle:
    wins = 0
    loses = 0

    def __init__(self):
        with open('config.json', 'r') as file:
            config = json.load(file)

        self.secret = config['secret']
        self.tgId = config['tgId']
        self.initData = config['initData']
        self.telegram_bot_token = config['telegram_bot_token']
        self.telegram_chat_id = config['telegram_chat_id']
        self.discord_webhook_url = config['discord_webhook_url']
        self.notify_telegram = config.get('notify_telegram', True)
        self.notify_discord = config.get('notify_discord', True)
        self.websocket: websockets.WebSocketClientProtocol = None
        self.battleId = ""
        self.superHit = False
        self.strike = {
            "defense": False,
            "attack": False
        }
        self.stop_event = asyncio.Event()

    def send_telegram_notification(self, message):
        if not self.notify_telegram:
            return

        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": message
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error Telegram ]\t: {e}")

    def send_discord_notification(self, message):
        if not self.notify_discord:
            return

        payload = {
            "content": message
        }
        try:
            response = requests.post(self.discord_webhook_url, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"🍓 {Fore.RED+Style.BRIGHT}[ Error Discord ]\t: {e}")

    async def sendHit(self):
        while not self.stop_event.is_set():
            if self.superHit:
                await asyncio.sleep(0.5)
                continue

            content = [
                "HIT",
                {
                    "battleId": self.battleId
                }
            ]
            try:
                await self.websocket.send(f"42{json.dumps(content)}")
            except:
                return
            await asyncio.sleep(0.14)

    async def listenerMsg(self):
        while not self.stop_event.is_set():
            try:
                data = await self.websocket.recv()
            except Exception as err:
                self.stop_event.set()
                return

            if data.startswith('42'):
                data = json.loads(data[2:])

                if data[0] == "HIT":
                    print(f"🤬 {Fore.CYAN + Style.BRIGHT}[ Fight ]: {self.player1['name']} ({data[1]['player1']['energy']}) 👀 ({data[1]['player2']['energy']}) {self.player2['name']}", flush=True)

                elif data[0] == "SET_SUPER_HIT_PREPARE":
                    self.superHit = True
                elif data[0] == "SET_SUPER_HIT_ATTACK_ZONE":
                    content = [
                        "SET_SUPER_HIT_ATTACK_ZONE",
                        {
                            "battleId": self.battleId,
                            "zone": randint(1, 4)
                        }
                    ]
                    await self.websocket.send(f"42{json.dumps(content)}")
                    self.strike['attack'] = True
                elif data[0] == "SET_SUPER_HIT_DEFEND_ZONE":
                    content = [
                        "SET_SUPER_HIT_DEFEND_ZONE",
                        {
                            "battleId": self.battleId,
                            "zone": randint(1, 4)
                        }
                    ]
                    await self.websocket.send(f"42{json.dumps(content)}")
                    self.strike['defense'] = True
                elif data[0] == "ENEMY_LEAVED":
                    return
                elif data[0] == "END":
                    if data[1]['result'] == "WIN":
                        Battle.wins += 1
                        result = f"🤖 @{self.id1} ⚔ @{self.id2}\n| 💀 {self.lvl1} ⚔ {self.lvl2}\n| 💰 {self.bal1} ⚔ {self.bal2}\n| 💥 {self.dm1} ⚔ {self.dm2}\n| ⚡ {self.en1} ⚔ {self.en2}\n| 👑 Victory  Reward: {data[1]['reward']} Coins"
                        print(f"🍏 {Fore.CYAN+Style.BRIGHT}[ Fight ]\t\t: [ Result ] {data[1]['result']} | [ Reward ] {data[1]['reward']} Coins")
                    else:
                        Battle.loses += 1
                        result = f"🤖 @{self.id1} ⚔ @{self.id2}\n| 💀 {self.lvl1} ⚔ {self.lvl2}\n| 💰 {self.bal1} ⚔ {self.bal2}\n| 💥 {self.dm1} ⚔ {self.dm2}\n| ⚡ {self.en1} ⚔ {self.en2}\n| 🏴‍☠️ Enemy  Loses: {data[1]['reward']} Coins"
                        print(f"🍎 {Fore.CYAN+Style.BRIGHT}[ Fight ]\t\t: [ Result ] {data[1]['result']} | [ Reward ] {data[1]['reward']} Coins")

                    # Perhitungan Win Rate
                    if Battle.wins == 0 and Battle.loses == 0:
                        winRate = 0
                    else:
                        winRate = (Battle.wins / (Battle.wins + Battle.loses)) * 100
                    battlesCount = Battle.wins + Battle.loses

                    # Kirim notifikasi
                    message = f"============[Result Battle]============\n| {result}\n============[ STATS ]============\n| ✍🏼 War: {split_chunk(str(battlesCount))} = Wins: {Battle.wins} = Loses: {Battle.loses} = Winrate: {winRate:.2f}%\n============[PIXELVERSE]============\n"
                    self.send_telegram_notification(message)
                    self.send_discord_notification(message)

                    await asyncio.sleep(0.5)
                    await self.websocket.recv()
                    self.stop_event.set()
                    return
                try:
                    if (self.strike['attack'] and not self.strike['defense']) or (self.strike['defense'] and not self.strike['attack']):
                        await self.websocket.recv()
                        await self.websocket.recv()
                    if self.strike['attack'] and self.strike['defense']:
                        await self.websocket.recv()
                        await self.websocket.send("3")
                        await self.websocket.recv()

                        self.superHit = False
                except:
                    pass

    async def connect(self):
        uri = "wss://api-clicker.pixelverse.xyz/socket.io/?EIO=4&transport=websocket"
        async with websockets.connect(uri) as websocket:
            self.websocket = websocket
            data = await websocket.recv()
            content = {
                "tg-id": self.tgId,
                "secret": self.secret,
                "initData": self.initData
            }

            await websocket.send(f"40{json.dumps(content)}")
            await websocket.recv()

            data = await websocket.recv()
            data = json.loads(data[2:])
            self.battleId = data[1]['battleId']
            self.player1 = {
                "name": data[1]['player1']['username']
            }
            self.player2 = {
                "name": data[1]['player2']['username']
            }
            self.id1 = data[1]['player1']['username']
            self.id2 = data[1]['player2']['username']
            self.lvl1 = data[1]['player1']['level']
            self.lvl2 = data[1]['player2']['level']
            self.bal1 = split_chunk(str(int(data[1]['player1']['balance'])))
            self.bal2 = split_chunk(str(int(data[1]['player2']['balance'])))
            self.en1 = split_chunk(str(int(data[1]['player1']['energy'])))
            self.en2 = split_chunk(str(int(data[1]['player2']['energy'])))
            self.dm1 = data[1]['player1']['damage']
            self.dm2 = data[1]['player2']['damage']

            print(f"🤪 {Fore.CYAN+Style.BRIGHT}[ Fight Profile ]\t: {Fore.RED+Style.BRIGHT}[ Username ] {data[1]['player1']['username']} {Fore.YELLOW+Style.BRIGHT}| {Fore.GREEN+Style.BRIGHT}[ Level ] {data[1]['player1']['level']} {Fore.YELLOW+Style.BRIGHT}| {Fore.BLUE+Style.BRIGHT}[ Balance ] {split_chunk(str(int(data[1]['player1']['balance'])))} {Fore.YELLOW+Style.BRIGHT}| {Fore.CYAN+Style.BRIGHT}[ Energy ] {split_chunk(str(int(data[1]['player1']['energy'])))} {Fore.YELLOW+Style.BRIGHT}| {Fore.MAGENTA+Style.BRIGHT}[ Damage ] {data[1]['player1']['damage']}")
            print(f"🤪 {Fore.CYAN+Style.BRIGHT}[ Fight Profile ]\t: {Fore.RED+Style.BRIGHT}[ Username ] {data[1]['player2']['username']} {Fore.YELLOW+Style.BRIGHT}| {Fore.GREEN+Style.BRIGHT}[ Level ] {data[1]['player2']['level']} {Fore.YELLOW+Style.BRIGHT}| {Fore.BLUE+Style.BRIGHT}[ Balance ] {split_chunk(str(int(data[1]['player2']['balance'])))} {Fore.YELLOW+Style.BRIGHT}| {Fore.CYAN+Style.BRIGHT}[ Energy ] {split_chunk(str(int(data[1]['player2']['energy'])))} {Fore.YELLOW+Style.BRIGHT}| {Fore.MAGENTA+Style.BRIGHT}[ Damage ] {data[1]['player2']['damage']}")

            for i in range(5, 0, -1):
                print(f"\r⏰ {Fore.YELLOW+Style.BRIGHT}[ Fight ]\t\t: Pertarungan Dimulai Dalam {i} Detik", end="\r", flush=True)
                await asyncio.sleep(1)

            print('')

            listenerMsgTask = asyncio.create_task(self.listenerMsg())
            hitTask = asyncio.create_task(self.sendHit())

            await asyncio.gather(listenerMsgTask, hitTask)
