import dateparser
import discord
import os

from discord.ext import commands

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    # Leaving this here in case we need a listener example
    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     channel = member.guild.system_channel
    #     if channel is not None:
    #         await channel.send('Welcome {0.mention}.'.format(member))


    # /reminder add <role> <time> <message>
    @commands.command()
    async def remind(self, ctx: commands.Context, *args, member: discord.Member = None):
        """Reminds user"""
        member = member or ctx.author
        message: discord.Message = ctx.message

        role = args[0]
        time = args[1]
        message = " ".join(args[2:])

        # Prefered '2017-07-30T10:00-07:00'
        # Prefered '2017-07-30T10:00:00-07:00'
        parsed_time = dateparser.parse(time,settings={'RETURN_AS_TIMEZONE_AWARE': True})
        time_formatted = parsed_time.strftime("%a, %b %d %Y, %I:%M:%S %p (%z)")

        # 2021-01-06 18:16 GMT-0700
        await ctx.send(f'Scheduling reminder for {time_formatted}')
