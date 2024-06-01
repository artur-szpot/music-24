from enums.commands import get_command_dictionary, CommandEnum
from enums.results import ResultEnum
from functions.execute.ArgsDict import ArgsDict
from functions.execute.arg_validation_errors import (
    NoArgumentsExpectedError,
    ComplexArgumentValidationError,
    ArgumentValidationError,
)
from functions.file_management.edit_db_file import edit_db_file
from functions.file_management.import_files import import_files, print_file_analysis
from functions.file_management.update_from_database import update_from_database
from functions.file_management.update_from_mp3 import update_from_mp3
from functions.querying.list_files import list_all_files

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
        return ExecutionResult(
            ResultEnum.Repeat,
            message,
        )


def parse_args(input_command):
    input_parts = input_command.split(" ")
    args_raw = input_parts[1:]
    args_raw.append("")
    args = []
    kwargs = {}
    flags = []
    current_flag = None
    current_arg = None
    for arg in args_raw:
        new_flag = None
        if arg.startswith("--"):
            if len(arg) == 2:
                return ExecutionResult.message(
                    [f'Incorrect flag usage: "--" lacks flag name']
                )
            if len(arg) == 3:
                return ExecutionResult.message(
                    [f'Incorrect flag usage: "{arg}" should have been "{arg[1:]}"']
                )
            new_flag = arg[2:]
        elif arg.startswith("-"):
            if len(arg) == 1:
                return ExecutionResult.message(
                    [f'Incorrect flag usage: "-" lacks flag name']
                )
            if len(arg) > 2:
                return ExecutionResult.message(
                    [f'Incorrect flag usage: "{arg}" should have been "-{arg}"']
                )
            new_flag = arg[1]
        elif arg.startswith('"'):
            if current_arg is not None:
                if len(arg) > 1:
                    return ExecutionResult.message(
                        [f"Parsing error: new quote opened before closing the last"]
                    )
                else:
                    arg = current_arg
            else:
                if arg == '""':
                    arg = ""
                else:
                    current_arg = arg[1:]
                    continue
        elif arg.endswith('"') and not arg.endswith('\\"'):
            if current_arg is None:
                return ExecutionResult.message(
                    [f"Parsing error: unpaired closing quote"]
                )
            current_arg += f" ${arg[:-1]}"
            arg = current_arg
        elif current_arg is not None:
            current_arg += f" ${arg}"
            continue

        if arg.startswith('"') and arg.endswith('"'):
            arg = arg[1:-1]
        arg = arg.replace('\\"', '"')

        if current_flag is None:
            if len(arg):
                args.append(arg)
        else:
            if new_flag is None and len(arg):
                values = kwargs.get(current_flag, [])
                values.append(arg)
                kwargs[current_flag] = values
            else:
                flags.append(current_flag)
                current_flag = new_flag
    return ArgsDict(args, kwargs, flags)


def execute_command(input_command):
    command = input_command.split(" ")[0]
    try:
        actual_command = get_commmand(command)
    except ValueError as error:
        return ExecutionResult.message([error])
    args_dict = parse_args(input_command)

    action_dict = {
        CommandEnum.Exit: ResultEnum.Return,
    }

    message_dict = {
        CommandEnum.ListFiles: list_all_files,
        CommandEnum.ImportFiles: import_files,
        CommandEnum.AnalyzeImport: print_file_analysis,
        CommandEnum.EditDatabaseFile: edit_db_file,
        CommandEnum.UpdateFromDatabase: update_from_database,
        CommandEnum.UpdateFromMp3: update_from_mp3,
    }

    action = action_dict.get(actual_command, ResultEnum.Repeat)
    try:
        message = message_dict.get(actual_command, lambda x: None)(args_dict)
    except NoArgumentsExpectedError:
        message = [f"Command {actual_command} accepts no arguments."]  # todo!
    except ComplexArgumentValidationError:
        message = [
            f"Incorrect arguments for command {actual_command} provided. Use the help command once available."
        ]  # todo!
    except ArgumentValidationError as e:
        message = [e]

    if action == ResultEnum.Repeat and message is None:
        return ExecutionResult.message([f"Command not yet handled: {command}"])

    return ExecutionResult(action, message)


def get_commmand(user_command):
    command = command_dictionary.get(user_command)
    if command is not None:
        return command
    raise ValueError(f"Unknown command: {user_command}")
