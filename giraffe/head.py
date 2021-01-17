import discord
import os

from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env file (located at giraffe/.env)

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

dirname = os.path.dirname(__file__)

cloud_config= {
        'secure_connect_bundle': os.path.join(dirname, '../secure-connect-giraffe-time.zip')
}
auth_provider = PlainTextAuthProvider(os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD'))
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()

from discord.ext import commands
from cogs.hello import Hello
from cogs.reminder import Reminder
from cogs.roles import Roles

client = discord.Client()

bot = commands.Bot(command_prefix='%')

# Add cogs here
bot.add_cog(Hello(bot,session))
bot.add_cog(Reminder(bot))
bot.add_cog(Roles(bot))

bot.run(os.getenv('DISCORD_TOKEN'))
