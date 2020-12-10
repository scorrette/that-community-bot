import discord

from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, cog):
        self.client.load_extension(f'cogs.{cog}')
        await ctx.send('Cog has been successfully loaded.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, cog):
        self.client.unload_extension(f'cogs.{cog}')
        await ctx.send('Cog has been successfully unloaded.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, cog):
        self.client.reload_extension(f'cogs.{cog}')
        await ctx.send('Cog has been successfully reloaded.')

    @load.error
    async def load_error(self, ctx, error):
        if isinstance(error.__cause__, commands.ExtensionAlreadyLoaded):
            await ctx.send('This cog is already loaded.')
        elif isinstance(error.__cause__, commands.ExtensionNotFound):
            await ctx.send('The cog entered is not valid.')
        elif isinstance(error.__cause__, commands.NotOwner):
            await ctx.send('You are not the owner of this bot, nice try...')
        else:
            await ctx.send(f'Some kind of error occured: `{type(error).__name__}: {error}`. Either report this as a bug or move on.')

    @unload.error
    @reload.error
    async def unload_error(self, ctx, error):
        if isinstance(error.__cause__, commands.ExtensionNotLoaded):
            await ctx.send('The cog isn\'t currently loaded; can\'t continue.')
        elif isinstance(error.__cause__, commands.ExtensionNotFound):
            await ctx.send('The cog entered is not valid.')
        elif isinstance(error.__cause__, commands.NotOwner):
            await ctx.send('You are not the owner of this bot, nice try...')
        else:
            await ctx.send(f'Some kind of error occured: `{type(error).__name__}: {error}`. Either report this as a bug or move on.')

def setup(client):
    client.add_cog(Owner(client))