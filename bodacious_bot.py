import discord

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


client.run('NzA0ODM4MTY5OTA0MDIxNTQ2.Xqi-Yw.LZPS_d9qjRsfcd4e_VHt3P2JvmI')