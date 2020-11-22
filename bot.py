#!/usr/bin/python3
import os
import logging

from discord.ext import commands
from dotenv import load_dotenv

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

bot = commands.Bot(command_prefix='!')

@bot.command(name='snom')
async def snom(message):
    msg = '<a:snomdance:779428824777228289>'
    await message.channel.send(msg)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.run(TOKEN)