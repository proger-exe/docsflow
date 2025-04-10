def return_to(command: str, *args, to_model: str):
    return f"{command} {' '.join(args)} TO_MODEL=> {to_model}"