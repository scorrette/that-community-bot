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
    guild_prefix = None

    if ctx.guild is not None:
        with closing(sqlite3.connect('guild_config.db')) as db:
            with closing(db.cursor()) as c:
                c.execute('''SELECT prefix
                             FROM guild_settings
                             WHERE guild_id=?
                        ''', (ctx.guild.id,))
                try:
                    guild_prefix = c.fetchone()[0]
                except:
                    pass
    
    return prefix if guild_prefix == None else guild_prefix

bot = commands.Bot(command_prefix=set_prefix)

@bot.command(help="Change the prefix of this bot on your server")
@commands.guild_only()
@commands.has_permissions(manage_guild=True)
async def prefix(ctx, prefix):
    with closing(sqlite3.connect('guild_config.db')) as db:
        with closing(db.cursor()) as c:
            c.execute('''SELECT *
                         FROM guild_settings
                         WHERE guild_id=?
                      ''', (ctx.guild.id,))
            if c.fetchone() == None:
                c.execute('''INSERT INTO guild_settings
                             VALUES (?, ?)
                          ''', (ctx.guild.id, prefix,))
            else:
                c.execute('''UPDATE guild_settings
                             SET prefix=?
                             WHERE guild_id=?
                          ''', (prefix, ctx.guild.id,))
        db.commit()
    
    msg = "Successfully changed prefix to `" + prefix + "`"
    await ctx.channel.send(msg)

@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        msg = ":x: You do not have permission to do that!"
        await ctx.channel.send(msg)
    elif isinstance(error, commands.NoPrivateMessage):
        msg = ":x: You can't use that command in my DMs!"
        await ctx.channel.send(msg)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)

bot.run(TOKEN)