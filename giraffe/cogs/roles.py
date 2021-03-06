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
    async def role_join(self, ctx: commands.Context, *, name: str=None):
        """Join a self-assignable role"""
        timeout = settings.timeout(ctx.guild, self._session)
        member = ctx.message.author
        if name is None:
            await ctx.send(f"{member.mention}, to join a self assignable role do `/join <role_name>`", delete_after=timeout)
        elif not get(ctx.guild.roles, name=name):
            await ctx.send(f"{member.mention}, the role `{name}` does not exist, was that a typo?", delete_after=timeout)
        else:
            role = get(ctx.guild.roles, name=name)
            if self._registered(role):
                try:
                    await member.add_roles(role)
                    await ctx.send(f"{member.mention} has joined **{name}**", delete_after=timeout)
                except:
                    await ctx.send(f"{member.mention}, **{name}** is set as self-assignable but cannot be assigned due to insufficient bot permissions, please contact an administrator", delete_after=timeout)
            else:
                await ctx.send(f"{member.mention}, **{name}** is not a self-assignable role. This incident will be reported.", delete_after=timeout)
        if settings.delete_user_command(ctx.guild, self._session):
            await ctx.message.delete()

    @commands.command(aliases=['leave'])
    async def role_leave(self, ctx: commands.Context, *, name: str=None):
        """Leave a self-assignable role"""

        timeout = settings.timeout(ctx.guild, self._session)
        member = ctx.message.author
        if name is None:
            await ctx.send(f"{member.mention}, to leave a self assignable role do `/leave <role_name>`", delete_after=timeout)
        elif not get(ctx.guild.roles, name=name):
            await ctx.send(f"{member.mention}, the role `{name}` does not exist, was that a typo?", delete_after=timeout)
        else:
            role = get(ctx.guild.roles, name=name)
            if self._registered(role):
                try:
                    await member.remove_roles(role)
                    await ctx.send(f"{member.mention} has left **{role.name}**", delete_after=timeout)
                except:
                    await ctx.send(f"{member.mention}, **{name}** is set as self-assignable but cannot be assigned due to insufficient bot permissions, please contact an administrator", delete_after=timeout)
            else:
                await ctx.send(f"{member.mention}, **{role.name}** is not a self-assignable role. This incident will be reported.", delete_after=timeout)
        await ctx.message.delete()

    @commands.command(aliases=['start_new_semester'])
    async def start_new_season(self, ctx: commands.Context):
        """Remove roles from all"""
        if settings.delete_user_command(ctx.guild, self._session):
            await ctx.message.delete()

        timeout = settings.timeout(ctx.guild, self._session)
        member = ctx.message.author
        if not self._is_admin(member):
            await ctx.send(f"{member.mention} is not in the Admins role, This incident will be reported.", delete_after=timeout)
            return

        await ctx.send(f"**Starting new semester**")
        rows = self._session.execute("SELECT role FROM giraffetime.roles WHERE guild=%s", (ctx.guild.id,)) 
        for row in rows:
            role_id = row.role
            removeCount = 0
            role = get(ctx.guild.roles, id=role_id)
            await ctx.send(f"Reseting **{role.name}**", delete_after=timeout)
            for member in role.members:
                try:
                    await member.remove_roles(role)
                    removeCount+=1
                except:
                    await ctx.send(f"An error occurred whilst removing {member.name} from role **{role.name}**.", delete_after=timeout)
            await ctx.send(f"Removed **{removeCount}** members from **{role.name}**", delete_after=timeout)
        await ctx.send(f"**Reset all members' self-assignable roles**", delete_after=timeout)

    @commands.command(aliases=['add', 'add_role'])
    async def role_add(self, ctx: commands.Context, *, name: str=None):
        """If the role exists, add it to the list of self-assignable roles. Otherwise create a self-assignable role."""
        if settings.delete_user_command(ctx.guild, self._session):
            await ctx.message.delete()



        timeout = settings.timeout(ctx.guild, self._session)
        member: discord.Member = ctx.author

        if not self._is_admin(member):
            await ctx.send(f'{member.mention} Only an administrator may perform this action.', delete_after=timeout)
            return

        if name is None:
            await ctx.send(f"{member.mention}, to add a self assignable role do `/add <role_name>`", delete_after=timeout)
            return

        guild = ctx.guild
        role: discord.Role = get(guild.roles, name=name)
        if role and self._registered(role):
            await ctx.send(f'{member.mention} Role **{name}** is already self-assignable.', delete_after=timeout)
            return

        if not role:
            if not settings.create_new_role(ctx.guild, self._session):
                await ctx.send(f'{member.mention} Role **{name}** does not exist.', delete_after=timeout)
                return
            role = await guild.create_role(name=name)
            await ctx.send(f'{member.mention} Role **{name}** does not exist. Creating new role **{name}**.', delete_after=timeout)
            # Confirmation prompt for creating a new role? Not asynchronous, so will not respond to other requests.
            # await ctx.send(f'{member.mention} Role **{name}** does not exist. Create a new role? (yes|no)')
            # def check(m: discord.Message):
            #     return m.author == member
            # try:
            #     confirmation = await self.bot.wait_for('message', check=check, timeout=5.0)
            #     content: str = confirmation.content.lower()
            #     if content == 'y' or content == 'yes':
            #         role = await guild.create_role(name=name)
            #         await ctx.send(f'{member.mention} Created role **{name}**.', delete_after=timeout)
            #     else:
            #         await ctx.send(f'{member.mention} Operation cancelled.', delete_after=timeout)
            #         return
            # except asyncio.TimeoutError:
            #     await ctx.send(f'{member.mention} Operation cancelled -- took too long to respond.', delete_after=timeout)
            #     return

        self._register(role)
        await ctx.send(f'{member.mention} Role **{name}** is now self-assignable.', delete_after=timeout)

    @commands.command(aliases=['remove', 'remove_role'])
    async def role_remove(self, ctx: commands.Context, *, name: str=None):
        """Remove a role from the list of self-assignables. Does not delete the role."""
        if settings.delete_user_command(ctx.guild, self._session):
            await ctx.message.delete()

        timeout = settings.timeout(ctx.guild, self._session)
        member: discord.Member = ctx.author
        if not member.guild_permissions.administrator:
            await ctx.send(f'{member.mention} Only an administrator may perform this action.', delete_after=timeout)
            return
        if name is None:
            await ctx.send(f"{member.mention}, to remove a self assignable role do `/remove <role_name>`", delete_after=timeout)
            return
        guild = ctx.guild
        role: discord.Role = get(guild.roles, name=name)

        if not role:
            await ctx.send(f'{member.mention} Role **{name}** does not exist.', delete_after=timeout)
            return

        if role and not self._registered(role):
            await ctx.send(f'{member.mention} Role **{name}** is already non-self-assignable.', delete_after=timeout)
            return

        self._unregister(role)
        await ctx.send(f'{member.mention} Role **{name}** is no longer self-assignable.', delete_after=timeout)

    @commands.command(aliases=['list', 'roles'])
    async def list_roles(self, ctx):
        """List all self-assignables roles"""
        settings.timeout(ctx.guild, self._session)
        if settings.delete_user_command(ctx.guild, self._session):
            await ctx.message.delete()

        timeout = settings.timeout(ctx.guild, self._session)

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
        await ctx.send(embed=embed, delete_after=timeout)
