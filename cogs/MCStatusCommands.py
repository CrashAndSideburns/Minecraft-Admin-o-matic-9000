import discord
from discord.ext import commands
import mcstatus_functions
import database_functions

class MCStatusCommands(commands.Cog, name='MC Status Commands'):
    def __init__(self, client):
        self.client = client

    @commands.command()
    #@commands.check(is_allowed_channel)
    async def online(self, ctx):
        await ctx.send(mcstatus_functions.playerNames(database_functions.get_ip(self.client, ctx), database_functions.get_port(self.client, ctx)))

def setup(client):
    client.add_cog(MCStatusCommands(client))
    print('MCStatus Commands are loaded!')