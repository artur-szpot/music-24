from enums.commands import CommandEnum, CommandDictionary
from enums.results import ResultEnum
from execute.db.create_test import create_test


def execute_command(command):
    try:
        actual_command = get_commmand(command)
    except ValueError as error:
        return ResultEnum.Repeat, error

    if actual_command == CommandEnum.Exit:
        return ResultEnum.Return, None
    elif actual_command == CommandEnum.CreateTest:
        create_test()
        return ResultEnum.Repeat, 'created test file'

    return ResultEnum.Repeat, f'Command not yet handled: {command}'


def get_commmand(user_command):
    command = CommandDictionary.get(user_command)
    if command is not None:
        return command
    raise ValueError(f'Unknown command: {user_command}')
