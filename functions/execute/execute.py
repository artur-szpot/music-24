from typing import Optional

from functions.commands.get_command_dictionary import get_command_dictionary
from functions.execute.ExecutionResult import ExecutionResult
from functions.execute.FullExecutionResult import FullExecutionResult
from functions.execute.arg_validation_errors import (
    NoArgumentsExpectedError,
    ComplexArgumentValidationError,
    ArgumentValidationError,
)
from functions.execute.args_parsing_errors import ArgsParsingError
from functions.execute.parse_args import parse_args
from libs.error_handling import error_message_to_string

command_dictionary = get_command_dictionary()


def execute_command(input_command: str) -> FullExecutionResult:
    user_command: str = input_command.split()[0]
    command_definition = command_dictionary.get(user_command)
    if command_definition is None:
        return FullExecutionResult(
            result=ExecutionResult.error_message(f"Unknown command: {user_command}")
        )
    actual_command = command_definition.verbs[0]

    error_message: Optional[str] = None
    result: Optional[ExecutionResult] = None
    try:
        args_dict = parse_args(input_command)
        args_dict = command_definition.args_validator.validate(args_dict)
        result = command_definition.function(args_dict)
    except NoArgumentsExpectedError:
        error_message = f"Command {actual_command} accepts no arguments."
        print(error_message)
        exit()
    except ComplexArgumentValidationError:
        error_message = f"Incorrect arguments provided for command {actual_command}. Use the help command to see details."
        # todo! give correct input for help
    except ArgumentValidationError as error:
        error_message = error_message_to_string(error)
    except ArgsParsingError as error:
        error_message = error_message_to_string(error)

    if error_message is not None:
        result = ExecutionResult.error_message(error_message)

    return FullExecutionResult(result=result, command=command_definition)


def get_command(user_command) -> Optional[str]:
    command = command_dictionary.get(user_command)
    if command is not None:
        return command.verbs[0]
    return None
