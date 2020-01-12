import discord
import json

client = discord.Client()
game = discord.Game("학습")
ledger = {}

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

@client.event
async def on_message(message):
    if message.author.bot:
        return None
    message_to_bot = message.content.split('$')
    if message_to_bot[0] == "HELP":
        if message_to_bot[1] == "GAMBLE":
            if message_to_bot[2] == "JOIN":
                await message.channel.send("갬블에 참가합니다. (기본 지급 100000BT)")
            if message_to_bot[2] == "SLOT":
                await message.channel.send("슬롯머신을 합니다. (소모 금액 500BT)")

    if message_to_bot[0] == "MONEY":
        if message_to_bot[1] == "ADD":
            if message_to_bot[2] not in ledger:
                ledger[message_to_bot[2]] = message_to_bot[3]
            else:
                ledger[message_to_bot[2]] += message_to_bot[3]
        if message_to_bot[1] == "SUB":
            if message_to_bot[2] not in ledger:
                ledger[message_to_bot[2]] = -message_to_bot[3]
            else:
                ledger[message_to_bot[2]] -= message_to_bot[3]

        with open("ledger.json", "w", encoding='utf-8') as ledger_json:
            ledger_json.write(json.dumps(ledger, ensure_ascii=False, indent=4))

client.run("your token")