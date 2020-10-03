import discord
from discord.ext import commands
import mcrcon_functions
import database_functions

class MCRCONCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return str(ctx.guild.id) in database_functions.get_allowed_channels(self.client, ctx)

    @commands.command()
    async def command(self, ctx, *, argument):
        await ctx.send(mcrcon_functions.executeCommand(database_functions.get_ip(self.client, ctx), database_functions.get_rcon_password(self.client, ctx), argument))


    @commands.command()
    async def seed(self, ctx):
        await ctx.send(mcrcon_functions.executeCommand(database_functions.get_ip(self.client, ctx), database_functions.get_rcon_password(self.client, ctx), '/seed'))

def setup(client):
    client.add_cog(MCRCONCommands(client))
    print('MCRCON Commands are loaded!')