import discord
from discord.ext import commands
from mcstatusFuncs import playerNames
from mcrconFuncs import executeCommand
import os
import sqlite3

BOT_TOKEN = os.getenv('BOT_TOKEN')

db = sqlite3.connect('data.db')
cursor = db.cursor()


def get_prefix(client, message):
    cursor.execute(f'SELECT prefix FROM guild_data WHERE guild_id={message.guild.id}')
    return cursor.fetchall()[0][0]

client = commands.Bot(command_prefix=get_prefix)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Running Minecraft Servers'))
    print('Bot is online!')


def get_ip(message):
    cursor.execute(f'SELECT ip FROM guild_data WHERE guild_id={message.guild.id}')
    return cursor.fetchall()[0][0]


def get_port(message):
    cursor.execute(f'SELECT port FROM guild_data WHERE guild_id={message.guild.id}')
    return cursor.fetchall()[0][0]


def get_rcon_password(message):
    cursor.execute(f'SELECT rcon_password FROM guild_data WHERE guild_id={message.guild.id}')
    return cursor.fetchall()[0][0]


def get_allowed_channels(message):
    cursor.execute(f'SELECT channel_id FROM allowed_channels WHERE guild_id={message.guild.id}')
    return [channel_id[0] for channel_id in cursor.fetchall()]


def is_allowed_channel(message):
    return str(message.channel.id) in get_allowed_channels(message)


def save():
    db.commit()



@client.event
async def on_guild_join(guild):
    cursor.execute(f'INSERT INTO guild_data (guild_id,prefix,ip,port,rcon_password) VALUES ("{guild.id}","mc.","","25565","")')
    save()


@client.event
async def on_guild_remove(guild):
    cursor.execute(f'DELETE FROM guild_data WHERE guild_id="{guild.id}""')
    save()


@client.command()
@commands.check(is_allowed_channel)
@commands.has_guild_permissions(administrator=True)
async def setip(ctx, ip):
    cursor.execute(f'UPDATE guild_data SET ip="{ip}" WHERE guild_id="{ctx.guild.id}"')
    save()


@client.command()
@commands.check(is_allowed_channel)
@commands.has_guild_permissions(administrator=True)
async def setport(ctx, port):
    cursor.execute(f'UPDATE guild_data SET "port={port}" WHERE guild_id="{ctx.guild.id}"')
    save()


@client.command()
@commands.check(is_allowed_channel)
@commands.has_guild_permissions(administrator=True)
async def setprefix(ctx, prefix):
    cursor.execute(f'UPDATE guild_data SET prefix="{prefix}" WHERE guild_id="{ctx.guild.id}"')
    save()


@client.command()
@commands.check(is_allowed_channel)
@commands.has_guild_permissions(administrator=True)
async def setrconpassword(ctx, rcon_password):
    cursor.execute(f'UPDATE guild_data SET rcon_password="{rcon_password}" WHERE guild_id="{ctx.guild.id}"')
    save()


@client.command()
@commands.has_guild_permissions(administrator=True)
async def channel(ctx, arg):
    if arg == "add":
        if str(ctx.channel.id) not in get_allowed_channels(ctx):
            cursor.execute(f'INSERT INTO allowed_channels (guild_id,channel_id) VALUES ("{ctx.guild.id}","{ctx.channel.id}")')
        else:
            pass
    elif arg == "remove":
        try:
            cursor.execute(f'DELETE FROM allowed_channels WHERE guild_id="{ctx.guild.id}" AND channel_id="{ctx.channel.id}"')
        except:
            pass
    save()


@client.command()
@commands.check(is_allowed_channel)
async def online(ctx):
    await ctx.send(playerNames(get_ip(ctx), get_port(ctx)))


@client.command()
@commands.check(is_allowed_channel)
@commands.has_guild_permissions(administrator=True)
async def command(ctx, *, argument):
    await ctx.send(executeCommand(get_ip(ctx), get_rcon_password(ctx), argument))


@client.command()
@commands.check(is_allowed_channel)
async def seed(ctx):
    await ctx.send(executeCommand(get_ip(ctx), get_rcon_password(ctx), '/seed'))


@client.command()
@commands.check(is_allowed_channel)
async def ip(ctx):
    await ctx.send(get_ip(ctx))


@client.command()
@commands.check(is_allowed_channel)
async def ping(ctx):
    await ctx.send(f'Current ping: {round(client.latency * 1000)}ms.')


@client.command()
@commands.check(is_allowed_channel)
async def github(ctx):
    await ctx.send('https://github.com/CrashAndSideburns/Minecraft-Admin-o-matic-9000')


@client.command()
@commands.check(is_allowed_channel)
@commands.has_guild_permissions(administrator=True)
async def dbdump(ctx):
    cursor.execute(f'SELECT * FROM guild_data JOIN allowed_channels ON guild_data.guild_id=allowed_channels.guild_id')
    await ctx.send(cursor.fetchall())


client.run(BOT_TOKEN)