import discord

from discord.ext import commands
from random import randint

class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(help="Flip a coin!")
    async def flip(self, ctx):
        await ctx.send("Heads!" if randint(0, 1) else "Tails!")

    @commands.command(help="Roll a n-sided dice")
    async def roll(self, ctx, n):
        result = randint(1, int(n))
        await ctx.send(f'The die landed on {result}!')
    
    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please input the number of sides of the die. Ex: `e!roll 6` to roll a six-sided die")

def setup(bot):
    bot.add_cog(Miscellaneous(bot))