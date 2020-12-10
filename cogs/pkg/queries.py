import os
import sqlite3

from dotenv import load_dotenv, find_dotenv
from contextlib import closing

load_dotenv(find_dotenv())
DATABASE = os.getenv('DATABASE')

def update_prefix(guild_id, prefix):
    success = True

    with closing(sqlite3.connect('guild_config.db')) as db:
        with closing(db.cursor()) as c:
            try:
                c.execute('''INSERT INTO guild_settings
                             VALUES (?, ?)
                          ''', (guild_id, prefix,))
            except sqlite3.IntegrityError:
                c.execute('''UPDATE guild_settings
                             SET prefix=?
                             WHERE guild_id=?
                          ''', (prefix, guild_id,))
            except sqlite3.OperationalError:
                c.execute('''CREATE TABLE guild_settings
                             (guild_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
                              prefix TEXT)
                          ''')
                c.execute('''INSERT INTO guild_settings
                             VALUES (?, ?)
                          ''', (guild_id, prefix,))
            else:
                success = False
        db.commit()
    
    return success