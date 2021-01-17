import discord
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
        self._session.execute("DELETE FROM giraffetime.roles WHERE guild_id=%s", (guild.id,))

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role: discord.Role):
        self._unregister(role)

    @commands.Cog.listener()
    async def on_guild_available(self, guild: discord.Guild):
        # Perhaps refresh the database? It might be that roles have gone out of sync. 
        pass

    ### COMMANDS ###

    @commands.command(aliases=['join'])
    async def role_join(self, ctx: commands.Context, *, name: str):
        """Join a role"""

        member = ctx.message.author
        if not get(ctx.guild.roles, name=name):
            await ctx.send(f"{member.mention}, the role `{name}` does not exist, was that a typo?", delete_after=settings.TIMEOUT)
        else:
            role = get(ctx.guild.roles, name=name)
            if self._registered(role):
                try:
                    await member.add_roles(role)
                    await ctx.send(f"{member.mention} has joined **{name}**", delete_after=settings.TIMEOUT)
                except:
                    await ctx.send(f"{member.mention}, **{name}** is set as self-assignable but cannot be assigned due to insufficient bot permissions, please contact an administrator", delete_after=settings.TIMEOUT)
            else:
                await ctx.send(f"{member.mention}, **{name}** is not a self-assignable role. This incident will be reported.", delete_after=settings.TIMEOUT)
        if settings.DELETE_USER_COMMAND:
            await ctx.message.delete()

    @commands.command(aliases=['leave'])
    async def role_leave(self, ctx: commands.Context, *, name: str):
        """Leave role"""

        member = ctx.message.author
        if not get(ctx.guild.roles, name=name):
            await ctx.send(f"{member.mention}, the role `{name}` does not exist, was that a typo?", delete_after=settings.TIMEOUT)
        else:
            role = get(ctx.guild.roles, name=name)
            if self._registered(role):
                try:
                    await member.remove_roles(role)
                    await ctx.send(f"{member.mention} has left **{role.name}**", delete_after=settings.TIMEOUT)
                except:
                    await ctx.send(f"{member.mention}, **{name}** is set as self-assignable but cannot be assigned due to insufficient bot permissions, please contact an administrator", delete_after=settings.TIMEOUT)
            else:
                await ctx.send(f"{member.mention}, **{role.name}** is not a self-assignable role. This incident will be reported.", delete_after=settings.TIMEOUT)
        await ctx.message.delete()

    @commands.command(aliases=['start_new_semester'])
    async def start_new_season(self, ctx: commands.Context):
        """Remove roles from all"""
        if settings.DELETE_USER_COMMAND:
            await ctx.message.delete()

        member = ctx.message.author
        if not self._is_admin(member):
            await ctx.send(f"{member.mention} is not in the Admins role, This incident will be reported.", delete_after=settings.TIMEOUT)
            return

        await ctx.send(f"**Starting new semester**")
        rows = self._session.execute("SELECT role FROM giraffetime.roles WHERE guild=%s", (ctx.guild.id,)) 
        for row in rows:
            role_id = row.role
            removeCount = 0
            role = get(ctx.guild.roles, id=role_id)
            await ctx.send(f"Reseting **{role.name}**", delete_after=settings.TIMEOUT)
            for member in role.members:
                try:
                    await member.remove_roles(role)
                    removeCount+=1
                except:
                    await ctx.send(f"An error occurred whilst removing {member.name} from role **{role.name}**.", delete_after=settings.TIMEOUT)
            await ctx.send(f"Removed **{removeCount}** members from **{role.name}**", delete_after=settings.TIMEOUT)
        await ctx.send(f"**Reset all members' self-assignable roles**", delete_after=settings.TIMEOUT)

    @commands.command(aliases=['add', 'add_role'])
    async def role_add(self, ctx: commands.Context, *, name: str):
        """If the role exists, add it to the list of self-assignable roles. Otherwise create a self-assignable role."""
        if settings.DELETE_USER_COMMAND:
            await ctx.message.delete()

        member: discord.Member = ctx.author
        if not self._is_admin(member):
            await ctx.send(f'{member.mention} Only an administrator may perform this action.', delete_after=settings.TIMEOUT)
            return

        guild = ctx.guild
        role: discord.Role = get(guild.roles, name=name)
        if role and self._registered(role):
            await ctx.send(f'{member.mention} Role **{name}** is already self-assignable.', delete_after=settings.TIMEOUT)
            return

        if not role:
            if not settings.CREATE_NEW_ROLE:
                await ctx.send(f'{member.mention} Role **{name}** does not exist.', delete_after=settings.TIMEOUT)
                return
            role = await guild.create_role(name=name)
            await ctx.send(f'{member.mention} Role **{name}** does not exist. Creating new role **{name}**.', delete_after=settings.TIMEOUT)
            # Confirmation prompt for creating a new role? Not asynchronous, so will not respond to other requests.
            # await ctx.send(f'{member.mention} Role **{name}** does not exist. Create a new role? (yes|no)')
            # def check(m: discord.Message):
            #     return m.author == member
            # try:
            #     confirmation = await self.bot.wait_for('message', check=check, timeout=5.0)
            #     content: str = confirmation.content.lower()
            #     if content == 'y' or content == 'yes':
            #         role = await guild.create_role(name=name)
            #         await ctx.send(f'{member.mention} Created role **{name}**.', delete_after=settings.TIMEOUT)
            #     else:
            #         await ctx.send(f'{member.mention} Operation cancelled.', delete_after=settings.TIMEOUT)
            #         return
            # except asyncio.TimeoutError:
            #     await ctx.send(f'{member.mention} Operation cancelled -- took too long to respond.', delete_after=settings.TIMEOUT)
            #     return

        self._register(role)
        await ctx.send(f'{member.mention} Role **{name}** is now self-assignable.', delete_after=settings.TIMEOUT)

    @commands.command(aliases=['remove', 'remove_role'])
    async def role_remove(self, ctx: commands.Context, *, name: str):
        """Remove a role from the list of self-assignables. Does not delete the role."""
        if settings.DELETE_USER_COMMAND:
            await ctx.message.delete()

        member: discord.Member = ctx.author
        if not member.guild_permissions.administrator:
            await ctx.send(f'{member.mention} Only an administrator may perform this action.', delete_after=settings.TIMEOUT)
            return

        guild = ctx.guild
        role: discord.Role = get(guild.roles, name=name)

        if not role:
            await ctx.send(f'{member.mention} Role **{name}** does not exist.', delete_after=settings.TIMEOUT)
            return

        if role and not self._registered(role):
            await ctx.send(f'{member.mention} Role **{name}** is already non-self-assignable.', delete_after=settings.TIMEOUT)
            return

        self._unregister(role)
        await ctx.send(f'{member.mention} Role **{name}** is no longer self-assignable.', delete_after=settings.TIMEOUT)

    @commands.command(aliases=['list', 'roles'])
    async def list_roles(self, ctx):
        if settings.DELETE_USER_COMMAND:
            await ctx.message.delete()
        roles = "```\n"
        rows = self._session.execute("SELECT role FROM giraffetime.roles WHERE guild=%s", (ctx.guild.id,))

        for row in rows:
            role_id = row.role
            removeCount = 0
            role = get(ctx.guild.roles, id=role_id)
            if role is not None:
                roles+=role.name + "\n"
        roles+="```"
        embed=discord.Embed(color=0xff1c8d)
        embed.add_field(name="Self Assignable Roles", value=roles, inline=True)
        await ctx.send(embed=embed, delete_after=settings.TIMEOUT)
