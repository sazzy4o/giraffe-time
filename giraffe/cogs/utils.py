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
    async def clear(self, ctx, *, count: str=10):
        """Clear chat, default clears last 10 messages"""
        if not ctx.message.author.guild_permissions.administrator:
            await ctx.send(f'{ctx.message.author.mention} Only an administrator may perform this action.')
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
        """Change timeout setting"""
        if ctx.message.author.guild_permissions.administrator:
            if timeout.lower() == "none":
                self.session.execute("INSERT INTO giraffetime.settings (guild, msg_timeout) VALUES (%s, NULL)", (ctx.guild.id,))
                await ctx.send(f"Set timeout to never expire")
            elif timeout.isnumeric():
                self.session.execute("INSERT INTO giraffetime.settings (guild, msg_timeout) VALUES (%s, %s)", (ctx.guild.id, int(timeout)))
                await ctx.send(f"Set timeout to {timeout} seconds")
            else:
                await ctx.send(f"Invalid input")

    @commands.command()
    async def remove_caller(self, ctx, *, new_caller: str):
        """Change remove caller setting"""
        if ctx.message.author.guild_permissions.administrator:
            if new_caller.lower() == "true":
                self.session.execute("INSERT INTO giraffetime.settings (guild, delete_user_cmd) VALUES (%s, True)", (ctx.guild.id,))
                await ctx.send(f"Set delete callers message to true")
            elif new_caller.lower() == "false":
                self.session.execute("INSERT INTO giraffetime.settings (guild, delete_user_cmd) VALUES (%s, False)", (ctx.guild.id,))
                await ctx.send(f"Set delete callers message to false")
            else:
                await ctx.send(f"Invalid input")

    @commands.command()
    async def create_missing_role(self, ctx, *, new_state: str):
        """Change create missing role setting"""
        if ctx.message.author.guild_permissions.administrator:
            if new_state.lower() == "true":
                self.session.execute("INSERT INTO giraffetime.settings (guild, create_roles) VALUES (%s, True)", (ctx.guild.id,))
                await ctx.send(f"Set create missing roles to true")
            elif new_state.lower() == "false":
                self.session.execute("INSERT INTO giraffetime.settings (guild, create_roles) VALUES (%s, False)", (ctx.guild.id,))
                await ctx.send(f"Set create missing roles to false")
            else:
                await ctx.send(f"Invalid input")
