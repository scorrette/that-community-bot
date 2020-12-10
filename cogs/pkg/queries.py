import os
import sqlite3

from dotenv import load_dotenv, find_dotenv
from contextlib import closing

load_dotenv(find_dotenv())
DATABASE = os.getenv('DATABASE')

def update_prefix(ctx, prefix):
    success = True

    with closing(sqlite3.connect(DATABASE)) as db:
        with closing(db.cursor()) as c:
            try:
                c.execute('''INSERT INTO guild_settings
                             VALUES (?, ?)
                          ''', (ctx.guild.id, prefix,))
            except sqlite3.IntegrityError:
                c.execute('''UPDATE guild_settings
                             SET prefix=?
                             WHERE guild_id=?
                          ''', (prefix, ctx.guild.id,))
            except sqlite3.OperationalError:
                c.execute('''CREATE TABLE guild_settings
                             (guild_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
                              prefix TEXT)
                          ''')
                c.execute('''INSERT INTO guild_settings
                             VALUES (?, ?)
                          ''', (ctx.guild.id, prefix,))
            else:
                success = False
        db.commit()
    
    return success

def set_counter(ctx, word):
    success = True

    with closing(sqlite3.connect(DATABASE)) as db:
        with closing(db.cursor()) as c:
            try:
                c.execute('''INSERT INTO counters
                             VALUES (?, ?)
                          ''', (ctx.author.id, word,))
            except sqlite3.IntegrityError:
                ctx.send('You already have a counter set for this word.')
            except sqlite3.OperationalError:
                c.execute('''CREATE TABLE counters
                             (user_id INTEGER PRIMARY KEY NOT NULL,
                              word TEXT,
                              count INTEGER NOT NULL DEFAULT 0,
                              UNIQUE(user_id, word))
                          ''')
                c.execute('''INSERT INTO counters
                             VALUES (?, ?)
                          ''', (ctx.author.id, word,))
            else:
                return False

    return success

def update_counter(ctx):
    success = True

    with closing(sqlite3.connect(DATABASE)) as db:
        with closing(db.cursor()) as c:
            try:
                c.execute('''SELECT word, count FROM counters
                             WHERE user_id=?
                          ''', (ctx.author.id,))
                
                result = c.fetchall()
                for row in result:
                    if row[0] in ctx.content.split():
                        c.execute('''UPDATE counters
                                     SET count=count + 1
                                     WHERE user_id=?
                                     AND word=?
                                  ''', (ctx.author.id, row[0]))

                        ctx.send(f'{ctx.author}\'s **{row[0]}** count: {row[1]}')
            except sqlite3.OperationalError:
                c.execute('''CREATE TABLE counters
                             (user_id INTEGER PRIMARY KEY NOT NULL,
                              word TEXT,
                              count INTEGER NOT NULL DEFAULT 0,
                              UNIQUE(user_id, word))
                          ''')
            else:
                success = False

    return success

def remove_counter(ctx, word):
    success = True

    with closing(sqlite3.connect(DATABASE)) as db:
        with closing(db.cursor()) as c:
            try:
                c.execute('''DELETE FROM counters
                             WHERE user_id=?
                             AND word=?
                          ''', (ctx.author.id, word))
                
                if c.rowcount == 0:
                    ctx.send('This word was not being counted.')
                else:
                    ctx.send('Successfully removed counter.')
            except sqlite3.OperationalError:
                c.execute('''CREATE TABLE counters
                             (user_id INTEGER PRIMARY KEY NOT NULL,
                              word TEXT,
                              count INTEGER NOT NULL DEFAULT 0,
                              UNIQUE(user_id, word))
                          ''')
            else:
                success = False

    return success