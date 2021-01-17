import discord
import os

from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file (located at giraffe/.env)

from discord.ext import commands
from cogs.hello import Hello
from cogs.role import *
client = discord.Client()

bot = commands.Bot(command_prefix='\\')

# Add cogs here
bot.add_cog(Hello(bot))
bot.add_cog(Role(bot))

bot.run(os.getenv('DISCORD_TOKEN'))
