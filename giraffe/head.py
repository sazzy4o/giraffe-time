import discord
import os

from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file (located at giraffe/.env)

from discord.ext import commands
from cogs.hello import Hello

settings = {}
with open('/app/settings.cfg', 'r') as configFile:
    for line in configFile:
        setting = line.split('=')
        settings[setting[0]] = setting[1].rstrip()

client = discord.Client()

bot = commands.Bot(command_prefix='/')
bot.add_cog(Hello(bot))
bot.run(os.getenv('DISCORD_TOKEN'))
