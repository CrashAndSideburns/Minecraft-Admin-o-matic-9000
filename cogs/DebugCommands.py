import discord
from discord.ext import commands

class DebugCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return ctx.author.id == 401472148796866560

    @commands.command()
    async def dbdump(self, ctx):
        self.client.cursor.execute(f'SELECT * FROM guild_data LEFT JOIN allowed_channels ON guild_data.guild_id=allowed_channels.guild_id')
        await ctx.send(self.client.cursor.fetchall())

def setup(client):
    client.add_cog(DebugCommands(client))
    print('Debug Commands are loaded!')