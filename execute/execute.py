from enums.commands import CommandEnum, get_command_dictionary
from enums.results import ResultEnum
from execute.db.edit_file import edit_file
from execute.db.import_files import import_files
from execute.db.list_files import list_files
from execute.db.create_test import create_test

command_dictionary = get_command_dictionary()


class ExecutionResult:
    def __init__(self, action, message=None):
        self.action = action
        self.message = message

    @staticmethod
    def action(action):
        return ExecutionResult(action)

    @staticmethod
    def message(message):
        return ExecutionResult(ResultEnum.Repeat, message, )


def execute_command(command):
    try:
        actual_command = get_commmand(command)
    except ValueError as error:
        return ExecutionResult.message([error])

    if actual_command == CommandEnum.Exit:
        return ExecutionResult.action(ResultEnum.Return)
    elif actual_command == CommandEnum.CreateTest:
        message = create_test()
        return ExecutionResult.message(message)
    elif actual_command == CommandEnum.ListFiles:
        message = list_files()
        return ExecutionResult.message(message)
    elif actual_command == CommandEnum.ImportFiles:
        message = import_files()
        return ExecutionResult.message(message)
    elif actual_command == CommandEnum.EditFile:
        message = edit_file('abc', {'path': "import\\Technimatic - Horizons [Flowidus & Tiki Taane] - Copy.mp3",
                                    "authors": ['Beethoven', 'Mozart']})
        return ExecutionResult.message(message)

    return ExecutionResult.message([f'Command not yet handled: {command}'])


def get_commmand(user_command):
    command = command_dictionary.get(user_command)
    if command is not None:
        return command
    raise ValueError(f'Unknown command: {user_command}')
