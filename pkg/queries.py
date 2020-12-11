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
        db.commit()
    
    return prefix

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

async def set_counter(ctx, word):
    success = True

    with closing(sqlite3.connect(DATABASE)) as db:
        with closing(db.cursor()) as c:
            try:
                c.execute('''INSERT INTO counters (user_id, word)
                             VALUES (?, ?)
                          ''', (ctx.author.id, word,))
                await ctx.send(f'Successfully set a counter for {ctx.author}: **{word}**.')
            except sqlite3.IntegrityError:
                await ctx.send('You already have a counter set for this word.')
            except sqlite3.OperationalError:
                c.execute('''CREATE TABLE counters
                             (user_id INTEGER NOT NULL,
                              word TEXT,
                              count INTEGER NOT NULL DEFAULT 0,
                              PRIMARY KEY(user_id, word),
                              UNIQUE(user_id, word))
                          ''')
                c.execute('''INSERT INTO counters (user_id, word)
                             VALUES (?, ?)
                          ''', (ctx.author.id, word,))
                await ctx.send(f'Successfully set a counter for {ctx.author}: **{word}**.')
            else:
                success = False
        db.commit()

    return success

async def update_counter(ctx):
    success = True

    with closing(sqlite3.connect(DATABASE)) as db:
        with closing(db.cursor()) as c:
            try:
                c.execute('''SELECT word, count FROM counters
                             WHERE user_id=?
                          ''', (ctx.author.id,))
                
                result = c.fetchall()
                for row in result:
                    i = 0
                    for word in ctx.content.split():
                        if row[0] == word:
                            c.execute('''UPDATE counters
                                         SET count=count + 1
                                         WHERE user_id=?
                                         AND word=?
                                    ''', (ctx.author.id, row[0]))
                            i += 1
                    if i > 0:
                        await ctx.channel.send(f'{ctx.author.name}\'s **{row[0]}** count: {row[1] + i}')
            except sqlite3.OperationalError:
                c.execute('''CREATE TABLE counters
                             (user_id INTEGER NOT NULL,
                              word TEXT,
                              count INTEGER NOT NULL DEFAULT 0,
                              PRIMARY KEY(user_id, word),
                              UNIQUE(user_id, word))
                          ''')
            else:
                success = False
        db.commit()

    return success

async def remove_counter(ctx, word):
    success = True

    with closing(sqlite3.connect(DATABASE)) as db:
        with closing(db.cursor()) as c:
            try:
                c.execute('''DELETE FROM counters
                             WHERE user_id=?
                             AND word=?
                          ''', (ctx.author.id, word))
                
                if c.rowcount == 0:
                    await ctx.send('This word was not being counted.')
                else:
                    await ctx.send('Successfully removed counter.')
            except sqlite3.OperationalError:
                c.execute('''CREATE TABLE counters
                             (user_id INTEGER NOT NULL,
                              word TEXT,
                              count INTEGER NOT NULL DEFAULT 0,
                              PRIMARY KEY(user_id, word),
                              UNIQUE(user_id, word))
                          ''')
            else:
                success = False
        db.commit()

    return success