import discord
import json
import random

client = discord.Client()
game = discord.Game("갬블")
ledger = {}
gamble_data = {}

try:
    print("ledger.json 의 내용을 불러옵니다.")
    with open("ledger.json", "r") as ledger_json:
        ledger = json.load(ledger_json)
except FileNotFoundError:
    print("ledger.json 을 찾지 못하였습니다.")
    print("ledger 를 초기화합니다.")
    ledger = {}


@client.event
async def on_ready():
    print('Bot Online')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(status=discord.Status.idle, activity=game)


spade = {
    1: '🂡',
    2: '🂢',
    3: '🂣',
    4: '🂤',
    5: '🂥',
    6: '🂦',
    7: '🂧',
    8: '🂨',
    9: '🂩',
    10: '🂪',
    11: '🂫',
    12: '🂭',
    13: '🂮'
}


@client.event
async def on_message(message):
    if message.author.bot:
        return None
    message_to_bot = message.content.split('$')

    if message_to_bot[0] == "HELP":
        if message_to_bot[1] == "GAMBLE":
            embed = discord.Embed()
            embed.add_field(name="GAMBLE$INIT", value="잔액을 초기화합니다. (기본 지급 100000BT)", inline=False)
            embed.add_field(name="GAMBLE$INDIAN$INT", value="인디안 포커를 시작합니다.", inline=True)
            embed.add_field(name="GAMBLE$INDIAN$BET$<베팅 금액>", value="베팅 금액만큼 베팅합니다.", inline=True)
            await message.channel.send(embed=embed)

    if message_to_bot[0] == "GAMBLE":
        if message_to_bot[1] == "INIT":
            ledger[str(message.author.id)] = 100000
            with open("ledger.json", "w", encoding='utf-8') as ledger_json:
                ledger_json.write(json.dumps(ledger, ensure_ascii=False, indent=4))
        if message_to_bot[1] == "INDIAN":
            if message_to_bot[2] == "INT":
                user = random.randrange(1, 14)
                cpu = random.randrange(1, 14)
                while user == cpu:
                    cpu = random.randrange(1, 14)
                await message.channel.send("CPU의 카드는 " + spade[cpu] + " 입니다.")
                gamble_data[str(message.author.id)] = {
                    'USER': user,
                    'CPU': cpu
                }
            if message_to_bot[2] == "BET":
                if str(message.author.id) in ledger:
                    user_bet = float(message_to_bot[3])
                    if user_bet < ledger[str(message.author.id)]:
                        cpu_bet = user_bet * random.random()
                        if str(message.author.id) in gamble_data:
                            if user_bet < 0:
                                await message.channel.send("빚을 내걸면 안되죠, 손님.")
                            else:
                                if gamble_data[str(message.author.id)]["CPU"] < gamble_data[str(message.author.id)]["USER"]:
                                    await message.channel.send("인디안 게임에서 승리하셨습니다.\n플레이어님께서는 " + str(cpu_bet) + "BT를 얻게 됩니다.")
                                    ledger[str(message.author.id)] += cpu_bet
                                    with open("ledger.json", "w", encoding='utf-8') as ledger_json:
                                        ledger_json.write(json.dumps(ledger, ensure_ascii=False, indent=4))
                                else:
                                    await message.channel.send("인디안 게임에서 패배하셨습니다.\n플레이어님께서는 " + str(user_bet) + "BT를 잃게 됩니다.")
                                    ledger[str(message.author.id)] -= user_bet
                                    with open("ledger.json", "w", encoding='utf-8') as ledger_json:
                                        ledger_json.write(json.dumps(ledger, ensure_ascii=False, indent=4))
                                del (gamble_data[str(message.author.id)])
                        else:
                            await message.channel.send("인디안 포커를 시작하지 않으셨습니다.")
                    else:
                        await message.channel.send("손님께서 걸 수 있을 만한 금액이 아닙니다.")
                else:
                    await message.channel.send("장부에 등록되어있지 않은 사용자 입니다.")

client.run("your token")
