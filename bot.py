#!/usr/bin/python3
import os
import discord

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

@bot.event
async def on_member_join(member):
    channel = bot.get_channel('818537648515448872') #change logging channel ID
    embed=discord.Embed(description=f"{member.mention} joined the server") #change helper role ID
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel('818537648515448872') #change logging channel ID
    embed=discord.Embed(description=f"{member.mention} left the server") #change helper role ID
    await channel.send(embed=embed)

@bot.event
async def on_raw_reaction_add(reaction, member):
    if reaction.emoji == 'thumbsup' and reaction.message.channel.id == 818537648515448872: #change channel ID 
        member.add_role(818549791009144892, reason=None, atomic=True) #change role ID

@bot.event
async def on_member_update(before, after):
    for role in after.roles:
        if role.id == 818549791009144892: #change new-member role ID
            channel = bot.get_channel('818537648515448872') #change verification channel ID
            embed=discord.Embed(description=f"{after.mention}, welcome to Herphub! <@&479309565956063234>") #change helper role ID
            await channel.send(embed=embed)
    

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(TOKEN)