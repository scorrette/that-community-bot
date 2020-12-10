import os
import sqlite3

from dotenv import load_dotenv, find_dotenv
from contextlib import closing

load_dotenv(find_dotenv())
DATABASE = os.getenv('DATABASE')

def get_prefix(ctx):
    prefix = tuple()

    with closing(sqlite3.connect(DATABASE)) as db:
        with closing(db.cursor()) as c:
            try:
                c.execute('''SELECT prefix
                             FROM guild_settings
                             WHERE guild_id=?
                          ''', (ctx.guild.id,))
                prefix += (c.fetchone()[0],)
            except sqlite3.OperationalError:
                c.execute('''CREATE TABLE guild_settings
                             (guild_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
                              prefix TEXT)
                          ''')
            except TypeError:
                pass
    
    return prefix