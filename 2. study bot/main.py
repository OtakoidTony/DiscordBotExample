import discord
import json

client = discord.Client()
game = discord.Game("학습")
database = {}

try:
    print("database.json 의 내용을 불러옵니다.")
    with open("database.json", "r") as database_json:
        database = json.load(database_json)
except FileNotFoundError:
    print("database.json 을 찾지 못하였습니다.")
    print("database 를 초기화합니다.")
    database = {}

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
    if message.content == "HELP$ADD":
        await message.channel.send("ADD$<사용자 발화 내용>$<채팅봇 발화 내용>")
    if message_to_bot[0] == "ADD":
        database[message_to_bot[1]] = message_to_bot[2]
        with open("database.json", "w", encoding='utf-8') as database_json:
            database_json.write(json.dumps(database, ensure_ascii=False, indent=4))
        await message.channel.send("학습하였습니다.")
    if message.content in database:
        await message.channel.send(database[message.content])

client.run("your token")