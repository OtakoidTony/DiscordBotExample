import discord

client = discord.Client()
game = discord.Game("핑퐁")                 # 상태메시지를 변경시 사용됩니다.

@client.event
async def on_ready():
    print('Bot Online')
    print(client.user.name)
    print(client.user.id)
    await client.change_presence(status=discord.Status.idle, activity=game)

@client.event
async def on_message(message):              # 새로운 메시지를 수신할 때,
    if message.author.bot:                  # 발신인이 자신이면
        return None                         # 아무것도 하지 않습니다.
    if message.content == "!ping":          # 사용자가 !ping이라고 전송하면
        await message.channel.send("pong")  # 봇이 pong이라고 응답합니다.

client.run("your token")