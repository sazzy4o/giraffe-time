import discord
import os

settings = {}
with open('../settings.cfg', 'r') as configFile:
    for line in configFile:
        setting = line.split('=')
        settings[setting[0]] = setting[1].rstrip()

client = discord.Client()
PREFIX = settings.get('COMMAND_PREFIX')
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith(PREFIX + 'hello'):
        await message.channel.send('Hello!')



client.run(settings.get('DISCORD_TOKEN'))
