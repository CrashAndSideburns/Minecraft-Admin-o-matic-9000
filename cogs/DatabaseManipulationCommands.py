import discord
from discord.ext import commands
import database_functions

class DatabaseManipulationCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def cog_check(self, ctx):
        return str(ctx.guild.id) in database_functions.get_allowed_channels(self.client, ctx)

    @commands.command()
    async def setip(self, ctx, ip):
        self.client.cursor.execute(f'UPDATE guild_data SET ip="{ip}" WHERE guild_id="{ctx.guild.id}"')
        self.client.db.commit()


    @commands.command()
    async def setport(self, ctx, port):
        self.client.cursor.execute(f'UPDATE guild_data SET "port={port}" WHERE guild_id="{ctx.guild.id}"')
        self.client.db.commit()


    @commands.command()
    async def setprefix(self, ctx, prefix):
        self.client.cursor.execute(f'UPDATE guild_data SET prefix="{prefix}" WHERE guild_id="{ctx.guild.id}"')
        self.client.db.commit()


    @commands.command()
    async def setrconpassword(self, ctx, rcon_password):
        self.client.cursor.execute(f'UPDATE guild_data SET rcon_password="{rcon_password}" WHERE guild_id="{ctx.guild.id}"')
        self.client.db.commit()


    @commands.command()
    async def channel(self, ctx, arg):
        if arg == "add":
            if str(ctx.channel.id) not in database_functions.get_allowed_channels(self.client, ctx):
                self.client.cursor.execute(f'INSERT INTO allowed_channels (guild_id,channel_id) VALUES ("{ctx.guild.id}","{ctx.channel.id}")')
            else:
                pass
        elif arg == "remove":
            try:
                self.client.cursor.execute(f'DELETE FROM allowed_channels WHERE guild_id="{ctx.guild.id}" AND channel_id="{ctx.channel.id}"')
            except:
                pass
        self.client.db.commit()


def setup(client):
    client.add_cog(DatabaseManipulationCommands(client))
    print('Database Manipulation Commands are loaded!')