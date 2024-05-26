from enums.commands import CommandEnum, get_command_dictionary
from enums.results import ResultEnum
from execute.db.create_test import create_test
from execute.db.edit_file import edit_file
from execute.db.import_files import import_files, print_file_analysis
from execute.db.list_files import list_all_files

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

    special_result = execute_special(actual_command)
    if special_result:
        return special_result

    action_dict = {
        CommandEnum.Exit: ResultEnum.Return,
    }

    message_dict = {
        CommandEnum.CreateTest: create_test,
        CommandEnum.ListFiles: list_all_files,
        CommandEnum.ImportFiles: import_files,
        CommandEnum.AnalyzeImport: print_file_analysis
    }

    action = action_dict.get(actual_command, ResultEnum.Repeat)
    message = message_dict.get(actual_command, lambda: None)()

    if action == ResultEnum.Repeat and message is None:
        return ExecutionResult.message([f'Command not yet handled: {command}'])

    return ExecutionResult(action, message)


def execute_special(actual_command):
    if actual_command == CommandEnum.EditFile:
        message = edit_file('abc', {'path': "import\\Technimatic - Horizons [Flowidus & Tiki Taane] - Copy.mp3",
                                    "authors": ['Nergal', 'Artur'], 'genres': ['duh', 'wubs']})
        return ExecutionResult.message(message)
    return None


def get_commmand(user_command):
    command = command_dictionary.get(user_command)
    if command is not None:
        return command
    raise ValueError(f'Unknown command: {user_command}')
