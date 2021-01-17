import discord
import os

from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, bot, session):
        self.bot = bot
        self.session = session
        self._last_member = None

    # Leaving this here in case we need a listener example
    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     channel = member.guild.system_channel
    #     if channel is not None:
    #         await channel.send('Welcome {0.mention}.'.format(member))

    @commands.command()
    async def hello(self, ctx: commands.Context, *args, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        message: discord.Message = ctx.message
        row = self.session.execute("select release_version from system.local").one()
        version = row.release_version
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'(DB Version - {version}) Hello {member.name}~')
        else:
            await ctx.send(f'(DB Version - {version}) Hello {member.name}... This feels familiar.')
        self._last_member = member

        await message.delete()