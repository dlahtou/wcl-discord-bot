import discord
from dad_jokes.dad_jokes.py import get_dad_joke()
from properties import DISCORD_BOT_TOKEN

client = discord.Client()

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        if message.author == 'RoudyRacoon':
            await message.channel.send('Hello loser!')
        else:
            await message.channel.send('Hello!')

    if message.content.startswith('$dad_joke'):
        await message.channel.send(get_dad_joke())

client.run(DISCORD_BOT_TOKEN)
