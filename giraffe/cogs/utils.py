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
    async def clear(self, ctx, *, count: str):
        """The chat has been cleared ~ Aquafina water bottle"""
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send(f'{member.mention} Only an administrator may perform this action.')
        messages = [] #Empty list to put all the messages in the log
        number = 0
        try:
            number = int(count) #Converting the amount of messages to delete to an integer
        except:
            await ctx.send(f'Please enter a number in the range of 1 to 99')
            return

        if number > 100 or number < 1:
            await ctx.send(f'Please enter a number in the range of 1 to 100')
            return

        messagesRaw = await ctx.message.channel.history(limit=number).flatten()
        for message in messagesRaw:
            if message.pinned == False:
                messages.append(message)

        await ctx.message.channel.delete_messages(messages)


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
