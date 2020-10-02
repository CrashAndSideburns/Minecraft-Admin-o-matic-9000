from mcrcon import MCRcon

def executeCommand(ip, password, commandString):
    """Executes a command via rcon. Returns the server's response to the command if there is one, and a different string if the server dows not reply."""
    try:
        with MCRcon(ip,password) as rcon:
            try:
                resp = rcon.command(commandString)
                if resp:
                    return resp
                else:
                    return 'The command was successfully executed.'
            except:
                return 'The bot was unable to execute the command.'
    except:
        return 'The bot was unable to contact the server.'