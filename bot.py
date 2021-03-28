#!/usr/bin/python3
import os
import discord
import aiomysql

from discord.ext import commands
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TOKEN = os.getenv('DISCORD_TOKEN')
HOST = os.getenv('MYSQL_HOST')
PORT = int(os.getenv('MYSQL_PORT'))
USER = os.getenv('MYSQL_USER')
PASSWORD = os.getenv('MYSQL_PASS')
DB = os.getenv('MYSQL_DB')

intents = discord.Intents.default()
intents.members = True

async def get_prefix(bot, ctx):
    prefixes = tuple()

    async with bot.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f'SELECT `prefix` FROM `prefixes` WHERE `guild_id`={ctx.guild.id}')
            _prefixes = await cur.fetchall()

            for prefix in _prefixes:
                prefixes += prefix

    return prefixes

async def set_prefix(bot, ctx):
    prefix = ('tcb!',)

    if ctx.guild is not None:
        prefix += await get_prefix(bot, ctx)

    return prefix

bot = commands.Bot(command_prefix = set_prefix, case_insensitive = True, intents=intents)

@commands.is_owner()
@bot.command()
async def query(ctx, *, q):
    async with bot.pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(q)
            res = await cur.fetchall()
            await ctx.send(str(res))

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    bot.pool = await aiomysql.create_pool(host=HOST, port=PORT, user=USER, password=PASSWORD, db=DB, loop=bot.loop)

@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.send(f'The command you entered does not exist. Use `tcb!help` to see a list of commands')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)