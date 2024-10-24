from typing import Optional, List

from functions.cache import cache
from functions.commands.CommandEnum import CommandEnum
from functions.commands.get_command_dictionary import get_command_dictionary
from functions.execute.args.system_kwargs import SystemKwargs, system_kwargs
from functions.execute.result.ExecutionResult import (
    ExecutionResult,
    ExecutionResultCategory,
)
from functions.execute.result.FullExecutionResult import FullExecutionResult
from functions.execute.validate.arg_validation_errors import (
    NoArgumentsExpectedError,
    ComplexArgumentValidationError,
    ArgumentValidationError,
)
from functions.execute.parse.args_parsing_errors import ArgsParsingError
from functions.execute.parse.parse_args import parse_args
from functions.settings.app_settings import app_settings
from libs.error_handling import error_message_to_string
from libs.strings import quoted

command_dictionary = get_command_dictionary()


class DisallowedCommandError(ValueError):
    pass


def execute_command(
    input_command_raw: str,
    allowed_commands: List[CommandEnum] = None,
    default_prefix: str = None,
) -> FullExecutionResult:
    if not input_command_raw or input_command_raw in [" ", "\t"]:
        return FullExecutionResult()
    input_command = app_settings.aliases.get(input_command_raw, input_command_raw)
    cache.log_command(input_command_raw)
    user_command: str = input_command.split()[0]
    command_definition = command_dictionary.get(user_command)
    if command_definition is None:
        if default_prefix is not None:
            return execute_command(
                f"{default_prefix} {input_command_raw}",
                allowed_commands=allowed_commands,
            )
        return FullExecutionResult(
            result=ExecutionResult.error_message(f"Unknown command: {user_command}")
        )
    if (
        allowed_commands is not None
        and command_definition.command not in allowed_commands
    ):
        raise DisallowedCommandError(f"Command disallowed at this time: {user_command}")
    actual_command = command_definition.verbs[0]

    error_message: Optional[str] = None
    result: Optional[ExecutionResult] = None
    message: Optional[str] = None
    custom_error_message: Optional[str] = None
    try:
        args_dict = parse_args(input_command)
        args_dict = command_definition.args_validator.validate(args_dict)
        message_raw = args_dict.get_kwarg(system_kwargs(SystemKwargs.Message))
        if message_raw:
            message = message_raw[0]
        custom_error_message_raw = args_dict.get_kwarg(
            system_kwargs(SystemKwargs.ErrorMessage)
        )
        if custom_error_message_raw:
            custom_error_message = custom_error_message_raw[0]
        result = command_definition.function(args_dict)
        if command_definition.following_commands is not None or (
            result is not None
            and result.category
            in [
                ExecutionResultCategory.Detail,
                ExecutionResultCategory.Query,
            ]
        ):
            result.following_commands = command_definition.following_commands
    except NoArgumentsExpectedError:
        error_message = f"Command {actual_command} accepts no arguments."
    except ComplexArgumentValidationError:
        error_message = (
            f"Incorrect arguments provided for command {actual_command}. Use the help command to see "
            f"details. "
        )
        # todo! give correct input for help
    except ArgumentValidationError as error:
        error_message = error_message_to_string(error)
    except ArgsParsingError as error:
        error_message = error_message_to_string(error)

    if error_message is not None:
        result = ExecutionResult.error_message(error_message)
    elif message is not None:
        result.set_message(message)
    elif custom_error_message is not None:
        result.set_error_message(custom_error_message)

    next_command = cache.get_next_command()
    if next_command:
        if message is not None:
            next_command += f"--message {quoted(message)}"
        elif custom_error_message is not None:
            next_command += f"--error-message {quoted(custom_error_message)}"
        return execute_command(next_command)

    return FullExecutionResult(result=result, command=command_definition)


def get_command(user_command) -> Optional[str]:
    command = command_dictionary.get(user_command)
    if command is not None:
        return command.verbs[0]
    return None
