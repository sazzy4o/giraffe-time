import discord
import os

from discord.ext import commands
from cogs.hello import Hello

settings = {}
with open('/app/settings.cfg', 'r') as configFile:
    for line in configFile:
        setting = line.split('=')
        settings[setting[0]] = setting[1].rstrip()

client = discord.Client()

bot = commands.Bot(command_prefix=settings.get('COMMAND_PREFIX'))
bot.add_cog(Hello(bot))
bot.run(settings.get('DISCORD_TOKEN'))
