import discord
from dad_jokes.dad_jokes import get_dad_joke
from roll.roll import roll
from properties import DISCORD_BOT_TOKEN

client = discord.Client()

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user or not message.content.startswith('/'):
        return
    
    print('{0}: {1}'.format(message.author, message.content))
 
    if message.content.startswith('/hello'):
        print('Sending hello!')
        if message.author == 'RoudyRacoon#8007':
            await message.channel.send('Hello loser!')
        else:
            await message.channel.send('Hello!')
    elif message.content.startswith('/dadjoke'):
        await message.channel.send(get_dad_joke())
    elif message.content.startswith('/roll'):
        print('Rolling!')
        await message.channel.send(roll())
    else:
        print('Invalid message, no response sent')

client.run(DISCORD_BOT_TOKEN)
