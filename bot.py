import discord
from discord.ext import commands
from mcstatusFuncs import playerNames
from mcrconFuncs import executeCommand
import os
import sqlite3

BOT_TOKEN = os.getenv('BOT_TOKEN')

# to fix
def get_prefix(client, message):
    return client.data[str(message.guild.id)]["prefix"]

# to fix
def get_ip(message):
    return client.data[str(message.guild.id)]["ip"]

# to fix
def get_port(message):
    return client.data[str(message.guild.id)]["port"]

# to fix
def get_rcon_password(message):
    return client.data[str(message.guild.id)]["rcon_password"]

# to fix
def get_allowed_channels(message):
    return client.data[str(message.guild.id)]['allowed_channels']

# to fix
def is_allowed_channel(message):
    return str(message.channel.id) in get_allowed_channels(message)

# to fix/remove (commit)
def save():
    with open('data.json', 'w') as f:
        json.dump(client.data, f, indent=4)


client = commands.Bot(command_prefix=get_prefix)

#add database opening/connection creation
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('Running Minecraft Servers'))
    print('Bot is online!')

#to fix
@client.event
async def on_guild_join(guild):
    client.data[str(guild.id)] = {}
    client.data[str(guild.id)]["prefix"] = "mc."
    client.data[str(guild.id)]["ip"] = ""
    client.data[str(guild.id)]["port"] = "25565"
    client.data[str(guild.id)]["rcon_password"] = ""
    client.data[str(guild.id)]["allowed_channels"] = []
    save()

#to fix (remove row)
@client.event
async def on_guild_remove(guild):
    client.data.pop(str(guild.id))
    save()

#to fix
@client.command()
@commands.check(is_allowed_channel)
@commands.has_guild_permissions(administrator=True)
async def setip(ctx, ip):
    client.data[str(ctx.guild.id)]["ip"] = ip
    save()

#to fix
@client.command()
@commands.check(is_allowed_channel)
@commands.has_guild_permissions(administrator=True)
async def setport(ctx, port):
    client.data[str(ctx.guild.id)]["port"] = port
    save()

#to fix
@client.command()
@commands.check(is_allowed_channel)
@commands.has_guild_permissions(administrator=True)
async def setprefix(ctx, prefix):
    client.data[str(ctx.guild.id)]["prefix"] = prefix
    save()

#to fix
@client.command()
@commands.check(is_allowed_channel)
@commands.has_guild_permissions(administrator=True)
async def setrconpassword(ctx, rcon_password):
    client.data[str(ctx.guild.id)]["rcon_password"] = rcon_password
    save()

#to fix (lots to do here)
@client.command()
@commands.has_guild_permissions(administrator=True)
async def channel(ctx, arg):
    if arg == "add":
        if str(ctx.channel.id) not in get_allowed_channels(ctx):
            client.data[str(ctx.guild.id)]["allowed_channels"].append(str(ctx.channel.id))
        else:
            pass
    if arg == "remove":
        try:
            client.data[str(ctx.guild.id)]["allowed_channels"].remove(str(ctx.channel.id))
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

#fix or remove and replace with FROM Servers SELECT *
@client.command()
@commands.check(is_allowed_channel)
@commands.has_guild_permissions(administrator=True)
async def jsondump(ctx):
    await ctx.send(client.data)


client.run(BOT_TOKEN)