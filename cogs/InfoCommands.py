import discord
from discord.ext import commands
import database_functions

class InfoCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return str(ctx.guild.id) in database_functions.get_allowed_channels(self.client, ctx)

    @commands.command()
    async def ip(self, ctx):
        await ctx.send(database_functions.get_ip(self.client, ctx))


    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Current ping: {round(self.client.latency * 1000)}ms.')


    @commands.command()
    async def github(self, ctx):
        await ctx.send('https://github.com/CrashAndSideburns/Minecraft-Admin-o-matic-9000')

def setup(client):
    client.add_cog(InfoCommands(client))
    print('Info Commands are loaded!')