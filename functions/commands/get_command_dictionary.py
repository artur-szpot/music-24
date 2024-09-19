from typing import Dict

from functions.commands.command_registry import command_registry
from functions.commands.definition.FunctionDefinition import FunctionDefinition


def get_command_dictionary() -> Dict[str, FunctionDefinition]:
    command_dictionary = {}

    for command in command_registry:
        for code in command_registry[command].verbs:
            if code in command_dictionary:
                raise KeyError(f"Repeated code {code} detected")
            command_dictionary[code] = command_registry[command]

    return command_dictionary
