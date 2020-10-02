from mcstatus import MinecraftServer

def playerNames(ip, port):

    """Returns a string listing all players online."""

    lookupString="{}:{}".format(ip, port)
    try:
        server = MinecraftServer.lookup(lookupString)
        query = server.query()
        if query.players.names:
            return "The server has the following players online: {}.".format(", ".join(query.players.names))
        else:
            return "There are currently no players online."
    except:
        return "The bot was unable to contact the server."