import discord

from discord.ext import commands
from discord.utils import get

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(aliases=['add', 'add_role'])
    async def role_add(self, ctx: commands.Context, *, name: str):
        """If the role exists, add it to the list of self assignable roles. Otherwise create a self assignable role."""

        member: discord.Member = ctx.author
        if not member.guild_permissions.administrator:
            await ctx.send(f'{member.mention} Only an administrator may perform this action.')
            return

        guild = ctx.guild
        role: discord.Role = get(ctx.guild.roles, name=name)

        # if role and role is self-assignable: # TODO: Check if the role is already self-assignable. REQUIRES DATABASE

        if not role:
            await ctx.send(f'{member.mention} Creating new self-assignable role **{name}**.')
            role = await guild.create_role(name=name)
        else:
            await ctx.send(f'{member.mention} Added **{name}** to the list of self-assignable roles.')

        # TODO: add role to list of self assignable roles. REQUIRES DATABASE

    @commands.command(aliases=['remove', 'remove_role'])
    async def role_remove(self, ctx: commands.Context, *, name: str):
        """Remove a role from the list of self-assignables. Does not delete the role."""

        member: discord.Member = ctx.author
        if not member.guild_permissions.administrator:
            await ctx.send(f'{member.mention} Only an administrator may perform this action.')
            return

        guild = ctx.guild
        role: discord.Role = get(ctx.guild.roles, name=name)

        # if role and role is self-assignable:
        # TODO: Check if the role is already self-assignable. REQUIRES DATABASE

        if not role:
            await ctx.send(f'{member.mention} Role **{name}** does not exist.')
            return
        # else if role is not self-assignable: # TODO: Check if the role is not self-assignable. REQUIRES DATABASE
            # await ctx.send(f'{member.mention} **{name}** has already been removed from the list of self-assignable roles.')

        await ctx.send(f'{member.mention} Removed {name} from the list of self-assignable roles.')
