import discord

from discord.ext import commands
from discord.utils import get

class Role(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=['join'])
    async def role_join(self, ctx):
        """set role"""
        usrArgs = ctx.message.content.split(' ', 1)[1]
        print(ctx.message.content.split(' ', 1)[1])
        if not get(ctx.guild.roles, name=usrArgs):
            await ctx.send("Role does not exist")
            return;
        else:
            # TODO: Check if role is self assignable in database
            role = get(ctx.guild.roles, name=usrArgs)
            member = ctx.message.author
            try:
                await member.add_roles(role)
                await ctx.send(f"{member.mention} has joined **{role.name}**")
            except:
                await ctx.send("Not enough permissions to set this role, this incident will be reported")

        # self.bot.delete_message(ctx.message)
