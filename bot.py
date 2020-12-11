#!/usr/bin/python3
import os
import logging

from discord.ext import commands
from dotenv import load_dotenv
from pkg.queries import get_prefix

def setup_logger(log_name, log_file, level=logging.WARNING):
    logger = logging.getLogger(log_name)
    logger.setLevel(level)

    handler = logging.FileHandler(filename=log_file, encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

    logger.addHandler(handler)

    return logger

if not os.path.isdir('./logs/'):
    os.mkdir('./logs/')
logger = setup_logger('discord', './logs/discord.log', logging.INFO)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

def set_prefix(bot, ctx):
    prefix = ('e!',)

    if ctx.guild is not None:
        prefix += get_prefix(ctx)
    
    return prefix

bot = commands.Bot(command_prefix = set_prefix, case_insensitive = True)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.channel.send(f'The command you entered does not exist. Use `{set_prefix(bot, ctx)[-1]}help` to see a list of commands')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)