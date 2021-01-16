import discord
import os

from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file (located at giraffe/.env)
# .env contents:
#   DISCORD_TOKEN=your discord token

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$test'):
        await message.channel.send('Test complete!')

client.run(os.getenv('DISCORD_TOKEN'))
