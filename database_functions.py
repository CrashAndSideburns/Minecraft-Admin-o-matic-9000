def get_ip(client, message):
    client.cursor.execute(f'SELECT ip FROM guild_data WHERE guild_id="{message.guild.id}"')
    return client.cursor.fetchall()[0][0]


def get_port(client, message):
    client.cursor.execute(f'SELECT port FROM guild_data WHERE guild_id="{message.guild.id}"')
    return client.cursor.fetchall()[0][0]


def get_rcon_password(client, message):
    client.cursor.execute(f'SELECT rcon_password FROM guild_data WHERE guild_id="{message.guild.id}"')
    return client.cursor.fetchall()[0][0]


def get_allowed_channels(client, message):
    client.cursor.execute(f'SELECT channel_id FROM allowed_channels WHERE guild_id="{message.guild.id}"')
    return [channel_id[0] for channel_id in client.cursor.fetchall()]