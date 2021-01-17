import discord
import asyncio
import settings

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

    @commands.command(aliases=['join'])
    async def role_join(self, ctx):
        """set role"""
        usrArgs = ctx.message.content.split(' ', 1)[1]

        member = ctx.message.author

        if not get(ctx.guild.roles, name=usrArgs):
            await ctx.send(f"{member.mention}, the role `{usrArgs}` does not exist, was that a typo?", delete_after=settings.TIMEOUT)
        else:
            # TODO: Check if role is self assignable in database
            role = get(ctx.guild.roles, name=usrArgs)
            try:
                await member.add_roles(role)
                await ctx.send(f"{member.mention} has joined **{role.name}**", delete_after=settings.TIMEOUT)
            except:
                await ctx.send(f"{member.mention}, **{role.name}** is not in the self assignable roles. This incident will be reported.", delete_after=settings.TIMEOUT)
        if settings.DELETE_USER_COMMAND:
            await ctx.message.delete()

    @commands.command(aliases=['leave'])
    async def role_leave(self, ctx):
        """set role"""
        usrArgs = ctx.message.content.split(' ', 1)[1]

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
        if self._is_admin(member):
            await ctx.send(f"**Starting new semester**")
            tempList = ["Minions", "Pokemon", "Sample Role 1", "ECE 404"]
            roles = []
            for item in tempList:
                newrole = get(ctx.guild.roles, name=item)
                if newrole:
                    roles.append(newrole)
            #TODO: Get roles that are self assignable from database
            for role in roles:
                removeCount = 0
                await ctx.send(f"Reseting **{role.name}**")
                for member in role.members:
                    try:
                        await member.remove_roles(role)
                        removeCount+=1
                    except:
                        await ctx.send(f"{member.mention}, **{role.name}** is not in the self assignable roles. This incident will be reported.")
                await ctx.send(f"removed **{removeCount}** members from **{role.name}**")
            await ctx.send(f"**Reset all members self assignable roles**")
            await ctx.message.delete()
        else:
            await ctx.send(f"{member.mention} is not in the Admins role, This incident will be reported.")