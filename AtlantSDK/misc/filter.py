

def check_handlers(handler: dict, command: dict):
    compiled = []

    for param in handler.keys():
        cmd_param = command.get(param)

        if not cmd_param and param:
            compiled.append(False)

        if handler[param] == cmd_param:
            compiled.append(True)
    
    if not compiled:
        return False
    return min(compiled)

