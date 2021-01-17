import dateparser
import datetime
import discord
import os
import uuid

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dataclasses import dataclass
from discord.ext import commands

@dataclass
class ReminderMessage:
    row_id: str
    role: str
    guild_id: int
    channel_id: int
    time: datetime
    message_text: str

async def send_message(bot,message:ReminderMessage):
    channel = bot.get_channel(message.channel_id)
    guild = bot.get_guild(message.guild_id)
    role = discord.utils.get(guild.roles,name=message.role)
    await channel.send(f"{role.mention} {message.message_text}")

class Reminder(commands.Cog):
    def __init__(self, bot, session):
        self.bot = bot
        self.session = session
        self.scheduler = AsyncIOScheduler()
        self.scheduler.start()

    def schedule_message(self, message: ReminderMessage):
        self.scheduler.add_job(send_message, 'date', run_date=message.time, args=[self.bot,message])

    # /reminder add <role> <time> <message>
    @commands.command()
    async def remind(self, ctx: commands.Context, *args, member: discord.Member = None):
        """Reminds user"""
        member = member or ctx.author
        message: discord.Message = ctx.message

        role = args[0]
        time = args[1]
        message_text = " ".join(args[2:])

        # Prefered '2017-07-30T10:00-07:00'
        # Prefered '2017-07-30T10:00:00-07:00'
        parsed_time = dateparser.parse(time,settings={'RETURN_AS_TIMEZONE_AWARE': True})
        time_formatted = parsed_time.strftime("%a, %b %d %Y, %I:%M:%S %p (%z)")

        row_id = uuid.uuid4()

        guild_id = ctx.guild.id
        channel_id = message.channel.id

        # 2021-01-06 18:16 GMT-0700
        self.session.execute(
            "INSERT INTO giraffetime.reminders (id,role,time,guild,channel,message) VALUES (%s,%s,%s,%s,%s,%s);", 
            (row_id,role,parsed_time.isoformat(),guild_id,channel_id,message_text)
        )

        reminder_message = ReminderMessage(
            row_id=row_id,
            role=role,
            time=parsed_time,
            guild_id=guild_id,
            channel_id=channel_id,
            message_text=message_text,
        )

        self.schedule_message(reminder_message)

        await ctx.send(f'Scheduled reminder for {time_formatted}')
