import discord
import sqlite3

from discord.ext import commands
from contextlib import closing

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Change the prefix of this bot on your server")
    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix):
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
        await ctx.send(msg)

    @prefix.error
    async def prefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            msg = ":x: You do not have permission to do that!"
            await ctx.send(msg)
        elif isinstance(error, commands.NoPrivateMessage):
            msg = ":x: You can't use that command in my DMs!"
            await ctx.send(msg)

def setup(client):
    client.add_cog(Admin(client))