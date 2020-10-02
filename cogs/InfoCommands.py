import discord
from discord.ext import commands
import database_functions

class InfoCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    #@commands.check(is_allowed_channel)
    async def ip(self, ctx):
        await ctx.send(database_functions.get_ip(self.client, ctx))


    @commands.command()
    #@commands.check(is_allowed_channel)
    async def ping(self, ctx):
        await ctx.send(f'Current ping: {round(self.client.latency * 1000)}ms.')


    @commands.command()
    #@commands.check(is_allowed_channel)
    async def github(self, ctx):
        await ctx.send('https://github.com/CrashAndSideburns/Minecraft-Admin-o-matic-9000')

def setup(client):
    client.add_cog(InfoCommands(client))
    print('Info Commands are loaded!')