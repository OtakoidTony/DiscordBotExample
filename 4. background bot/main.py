import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    print('Bot Online')
    print(client.user.name)
    print(client.user.id)

async def my_background_task():
    await client.wait_until_ready()
    while not client.is_closed():
        game = discord.Game("핑")
        await client.change_presence(status=discord.Status.idle, activity=game)
        await asyncio.sleep(1)
        game = discord.Game("퐁")
        await client.change_presence(status=discord.Status.idle, activity=game)
        await asyncio.sleep(1)

client.loop.create_task(my_background_task())
client.run("your token")