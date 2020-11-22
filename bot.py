#!/usr/bin/python3
import os
import logging
import sqlite3

from discord.ext import commands
from dotenv import load_dotenv
from contextlib import closing

with closing(sqlite3.connect('guild_config.db')) as db:
    with closing(db.cursor()) as c:
        c.execute('''CREATE TABLE IF NOT EXISTS guild_settings
                     (guild_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
                      prefix TEXT)
                  ''')

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
    prefix = '!'

    with closing(sqlite3.connect('guild_config.db')) as db:
        with closing(db.cursor()) as c:
            c.execute('''SELECT prefix
                         FROM guild_settings
                         WHERE guild_id=?
                      ''', (ctx.guild.id,))
            try:
                guild_prefix = c.fetchone()[0]
            except:
                guild_prefix = None
    
    return prefix if guild_prefix == None else guild_prefix

bot = commands.Bot(command_prefix=set_prefix)

@bot.command()
async def prefix(ctx, prefix):
    print("Attempting to change prefix for guild: ", ctx.guild.id, " to ", prefix)
    with closing(sqlite3.connect('guild_config.db')) as db:
        with closing(db.cursor()) as c:
            c.execute('''SELECT *
                         FROM guild_settings
                         WHERE guild_id=?
                      ''', (ctx.guild.id,))
            if c.fetchone() == None:
                print("Guild was not previously found in the database, adding both guild id and prefix")
                c.execute('''INSERT INTO guild_settings
                             VALUES (?, ?)
                          ''', (ctx.guild.id, prefix,))
                print("Successfully changed prefix to ", prefix, " for ", ctx.guild.id)
            else:
                print("Guild found previously in database, updating prefix")
                c.execute('''INSERT INTO guild_settings
                             VALUES (?)
                             WHERE guild_id=?
                          ''', (prefix, ctx.guild.id,))
                print("Successfully changed prefix to ", prefix, " for ", ctx.guild.id)
        db.commit()

@bot.command()
async def snom(ctx):
    msg = '<a:snomdance:779428824777228289>'
    await ctx.channel.send(msg)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.run(TOKEN)