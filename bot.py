import discord
from discord.ext import commands
import os
import sqlite3

BOT_TOKEN = os.getenv('BOT_TOKEN')

cogs = ['cogs.DatabaseManipulationCommands',
        'cogs.DebugCommands',
        'cogs.InfoCommands',
        'cogs.MCRCONCommands',
        'cogs.MCStatusCommands']

def get_prefix(client, message):
    client.cursor.execute(f'SELECT prefix FROM guild_data WHERE guild_id="{message.guild.id}"')
    return client.cursor.fetchall()[0][0]

client = commands.Bot(command_prefix=get_prefix)

client.db = sqlite3.connect('data.db')
client.cursor = client.db.cursor()


@client.event
async def on_ready():
    for guild in client.guilds:
        client.cursor.execute(f'''
            SELECT * FROM guild_data WHERE guild_id="{guild.id}"
        ''')
        if not client.cursor.fetchone():
            client.cursor.execute(f'''
                INSERT INTO guild_data(guild_id,prefix,ip,port,rcon_password)
                VALUES ("{guild.id}","mc.","","25565","")
            ''')
    client.db.commit()

    await client.change_presence(activity=discord.Game('Running Minecraft Servers'))
    print('Bot is online!')


if __name__ == '__main__':
    for cog in cogs:
        try:
            client.load_extension(cog)
        except Exception:
            print(f'Failed to load {cog}.')


@client.event
async def on_guild_join(guild):
    client.cursor.execute(f'INSERT INTO guild_data (guild_id,prefix,ip,port,rcon_password) VALUES ("{guild.id}","mc.","","25565","")')
    client.db.commit()


@client.event
async def on_guild_remove(guild):
    client.cursor.execute(f'DELETE FROM guild_data WHERE guild_id="{guild.id}"')
    client.db.commit()


client.run('NzQxMTMwNjAwNTA0NjIzMTU0.XyzFqA.xWxz-05IZSm-HvkM0kkofRVhfI4')