#!/usr/bin/python3
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = 'tcb!', case_insensitive = True)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# @bot.event
# async def on_message_edit(before, after):
#     await bot.process_commands(after)

# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.channel.send(f'The command you entered does not exist. Use `{set_prefix(bot, ctx)[-1]}help` to see a list of commands')

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)