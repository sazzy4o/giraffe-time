import discord
import os
import settings

from discord.ext import commands

class Utils(commands.Cog):
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

    @commands.command(aliases=['prune', 'purge'])
    async def clear(self, ctx):
        """The chat has been cleared ~ Aquafina water bottle"""
        await ctx.send("." + "\n"*1500 +"The chat has been cleared ~ Aquafina water bottle")

    @commands.command()
    async def set_timeout(self, ctx, *, timeout: str):
        """The chat has been cleared ~ Aquafina water bottle"""
        if ctx.message.author.guild_permissions.administrator:
            if timeout.lower() == "none":
                settings.TIMEOUT = None
                await ctx.send(f"Set timeout to never expire")
            elif timeout.isnumeric():
                settings.TIMEOUT = int(timeout)
                await ctx.send(f"Set timeout to {timeout} seconds")
            else:
                await ctx.send(f"Invalid input")

    @commands.command()
    async def remove_caller(self, ctx, *, new_caller: str):
        """The chat has been cleared ~ Aquafina water bottle"""
        if ctx.message.author.guild_permissions.administrator:
            if new_caller.lower() == "true":
                settings.DELETE_USER_COMMAND = True
                await ctx.send(f"Set delete callers message to true")
            elif new_caller.lower() == "false":
                settings.DELETE_USER_COMMAND = False
                await ctx.send(f"Set delete callers message to false")
            else:
                await ctx.send(f"Invalid input")

    @commands.command()
    async def create_missing_role(self, ctx, *, new_state: str):
        """The chat has been cleared ~ Aquafina water bottle"""
        if ctx.message.author.guild_permissions.administrator:
            if new_state.lower() == "true":
                settings.CREATE_NEW_ROLE = True
                await ctx.send(f"Set create missing roles to true")
            elif new_state.lower() == "false":
                settings.CREATE_NEW_ROLE = False
                await ctx.send(f"Set create missing roles to false")
            else:
                await ctx.send(f"Invalid input")
