import discord
from properties import API_TOKEN

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
            await message.channel.sesnd('Hello loser!')
        else:
            await message.channel.send('Hello!')


client.run(API_TOKEN)