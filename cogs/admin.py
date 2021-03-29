import discord

from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def add_prefix(self, ctx, prefix):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f'INSERT INTO `prefixes` (`guild_id`, `prefix`) VALUES ({ctx.guild.id}, \'{prefix}\')')
                await conn.commit()

        await ctx.send(f'`{prefix}` has been added to the prefix list.')

    async def list_prefixes(self, ctx):
        desc = "Below is a list of prefixes set for your server:\n"
        embed = discord.Embed(title="Prefixes", description=desc, color=0xba60f0)

        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f'SELECT `prefix` FROM `prefixes` WHERE `guild_id`={ctx.guild.id}')
                prefixes = await cur.fetchall()

                for i in range(len(prefixes)):
                    desc += prefixes[i]
                    if not i == len(prefixes) - 1:
                        desc += '\n'

        await ctx.send(embed=embed)

    async def remove_prefix(self, ctx, prefix):
        async with self.bot.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f'DELETE FROM `prefixes` WHERE `guild_id`={ctx.guild.id} AND `prefix`=\'{prefix}\'')
                await conn.commit()

        await ctx.send(f'`{prefix}` has been removed from the prefix list.')

    @commands.command(help="Modify server prefixes")
    async def prefix(self, ctx, option, prefix = None):
        if option.lower() == 'add':
            if prefix == None:
                await ctx.send('This command expects a prefix to be passed to it.')
            else: await add_prefix(self, ctx, prefix)
        elif option.lower() == 'list':
            await list_prefixes(self, ctx)
        elif option.lower() == 'remove':
            if prefix == None:
                await ctx.send('This command expects a prefix to be passed to it.')
            else: await remove_prefix(self, ctx, prefix)
        else:
            await ctx.send('You must provide either add, list, or remove as an option.')

def setup(bot):
    bot.add_cog(Admin(bot))