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

        member = ctx.message.author

        if not get(ctx.guild.roles, name=usrArgs):
            await ctx.send(f"{member.mention}, the role `{usrArgs}` does not exist, was that a typo?")
        else:
            # TODO: Check if role is self assignable in database
            role = get(ctx.guild.roles, name=usrArgs)
            try:
                await member.add_roles(role)
                await ctx.send(f"{member.mention} has joined **{role.name}**")
            except:
                await ctx.send(f"{member.mention}, **{role.name}** is not in the self assignable roles. This incident will be reported.")
        await ctx.message.delete()

    @commands.command(aliases=['leave'])
    async def role_leave(self, ctx):
        """set role"""
        usrArgs = ctx.message.content.split(' ', 1)[1]
        print(ctx.message.content.split(' ', 1)[1])

        member = ctx.message.author

        if not get(ctx.guild.roles, name=usrArgs):
            await ctx.send(f"{member.mention}, the role `{usrArgs}` does not exist, was that a typo?")
        else:
            # TODO: Check if role is self assignable in database
            role = get(ctx.guild.roles, name=usrArgs)
            try:
                await member.remove_roles(role)
                await ctx.send(f"{member.mention} has left **{role.name}**")
            except:
                await ctx.send(f"{member.mention}, **{role.name}** is not in the self assignable roles. This incident will be reported.")
        await ctx.message.delete()

    @commands.command(aliases=['start_new_semester'])
    async def start_new_season(self, ctx):
        """set role"""
        member = ctx.message.author
        if ctx.message.author.guild_permissions.administrator:
            await ctx.send(f"Starting new semester")
            tempList = ["Minions", "Pokemon", "Sample Role 1", "ECE 404"]
            roles = []
            for item in tempList:
                newrole = get(ctx.guild.roles, name=item)
                if newrole:
                    print(str(newrole.position))
                    roles.append(newrole)
            #TODO: Get roles that are self assignable from database
            for role in roles:
                removeCount = 0
                for member in role.members:
                    await ctx.send(f"Reseting **{role.name}**")
                    try:
                        await member.remove_roles(role)
                        removeCount+=1
                    except:
                        await ctx.send(f"{member.mention}, **{role.name}** is not in the self assignable roles. This incident will be reported.")
                await ctx.send(f"removed **{removeCount}** members from **{role.name}**")
            await ctx.send(f"Reset all self assignable roles")
            await ctx.message.delete()
        else:
            await ctx.send(f"{member.mention} is not in the Admins role, This incident will be reported.")
