import discord
import asyncio

from discord.ext import commands
from discord.utils import get
from cassandra.cluster import ResultSet

class Roles(commands.Cog):
    def __init__(self, bot, session):
        self._bot = bot
        self._session = session

    def _is_admin(self, member: discord.Member) -> bool:
        return member.guild_permissions.administrator

    ### SELF-ASSIGNABLE ROLE MANAGEMENT ###

    def _registered(self, role: discord.Role) -> bool:
        """Return True if the role in the guild is self-assignable, False otherwise."""
        if not role:
            return False
        row: ResultSet = self._session.execute("SELECT * FROM giraffetime.roles WHERE guild=%s AND role=%s", (role.guild.id, role.id))
        return bool(row)

    def _register(self, role: discord.Role):
        """Make a role self-assignable."""
        guild: discord.Guild = role.guild
        self._session.execute("INSERT INTO giraffetime.roles (guild, role) VALUES (%s,%s)", (guild.id, role.id))

    def _unregister(self, role: discord.Role):
        """Makes a role no longer self-assignable."""
        self._session.execute("DELETE FROM giraffetime.roles WHERE guild=%s AND role=%s", (role.guild.id, role.id))

    ### LISTENERS ###

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        self._session.execute("DELETE FROM giraffetime.roles WHERE guild_id=%s", guild.id)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        self._unregister(role)

    @commands.Cog.listener()
    async def on_guild_available(self, guild: discord.Guild):
        # Perhaps refresh the database? It might be that roles have gone out of sync. 
        pass

    ### COMMANDS ###

    @commands.command(aliases=['add', 'add_role'])
    async def role_add(self, ctx: commands.Context, *, name: str):
        """If the role exists, add it to the list of self-assignable roles. Otherwise create a self-assignable role."""

        member: discord.Member = ctx.author
        if not self._is_admin(member):
            await ctx.send(f'{member.mention} Only an administrator may perform this action.')
            return

        guild = ctx.guild
        role: discord.Role = get(guild.roles, name=name)
        if role and self._registered(role):
            await ctx.send(f'{member.mention} Role **{name}** is already self-assignable.')
            return

        if not role:
            role = await guild.create_role(name=name)
            await ctx.send(f'{member.mention} Role **{name}** does not exist. Creating new role **{name}**.')
            # Confirmation prompt for creating a new role? Not asynchronous, so will not respond to other requests.
            # await ctx.send(f'{member.mention} Role **{name}** does not exist. Create a new role? (yes|no)')
            # def check(m: discord.Message):
            #     return m.author == member
            # try:
            #     confirmation = await self.bot.wait_for('message', check=check, timeout=5.0)
            #     content: str = confirmation.content.lower()
            #     if content == 'y' or content == 'yes':
            #         role = await guild.create_role(name=name)
            #         await ctx.send(f'{member.mention} Created role **{name}**.')
            #     else:
            #         await ctx.send(f'{member.mention} Operation cancelled.')
            #         return
            # except asyncio.TimeoutError:
            #     await ctx.send(f'{member.mention} Operation cancelled -- took too long to respond.')
            #     return 

        self._register(role)
        await ctx.send(f'{member.mention} Role **{name}** is now self-assignable.')

    @commands.command(aliases=['remove', 'remove_role'])
    async def role_remove(self, ctx: commands.Context, *, name: str):
        """Remove a role from the list of self-assignables. Does not delete the role."""

        member: discord.Member = ctx.author
        if not member.guild_permissions.administrator:
            await ctx.send(f'{member.mention} Only an administrator may perform this action.')
            return

        guild = ctx.guild
        role: discord.Role = get(guild.roles, name=name)

        if not role:
            await ctx.send(f'{member.mention} Role **{name}** does not exist.')
            return

        if role and not self._registered(role):
            await ctx.send(f'{member.mention} Role **{name}** is already non-self-assignable.')
            return

        self._unregister(role)
        await ctx.send(f'{member.mention} Role **{name}** is no longer self-assignable.')
