def make_an_update(raw_str: str, state=""):
    command, where = raw_str.split("TO_MODEL=>")
    command = command.strip()
    where = where.strip()

    command_params_list = command.split()
    command_params = ' '.join(command_params_list[1:])

    if not command_params_list[1:] and state:
        return ({"command": command_params_list[0], "state": state}, where)

    elif not command_params_list[1:] and not state:
        return ({"command": command_params_list[0]}, where)

    elif command_params_list[1:] and state:
        return ({"command": command_params_list[0], "args": command_params, "state": state}, where)
    
    elif command_params_list[1:] and not state:
        return ({"command": command_params_list[0], "args": command_params}, where)

    else:
        return ({"command": command_params_list[0]}, where)
