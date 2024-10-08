from typing import List

from functions.commands.command_registry import command_registry
from functions.commands.definition.ArgsDict import ArgsDict
from functions.execute.args_parsing_errors import ArgsParsingError
from functions.help.help_definition import help_definition
from functions.cache.cache import query_cache


def parse_args(input_command: str) -> ArgsDict:
    input_parts = input_command.split()
    command = input_parts[0]
    args_raw = input_parts[1:]
    args = parse_args_exe(args_raw)
    last_result = query_cache.get("last")
    if command in help_definition().verbs:
        args.system = {
            "command_registry": command_registry,
            "current_file": last_result.get_file(index - 1),
        }
    return args


def parse_args_exe(args_raw: List[str]) -> ArgsDict:
    # Ensure the processing will end on an empty token.
    args_raw.append("")

    # Initialize end products.
    args = []
    flags_and_kwargs = {}

    # Initialize temps.
    current_flag = None
    current_arg = None

    for arg in args_raw:
        # If it starts with dashes, set the new_flag value to the name of the flag/kwarg.
        new_flag = None
        if arg.startswith("--"):
            if len(arg) == 2:
                raise ArgsParsingError(f'Incorrect flag usage: "--" lacks flag name')
            if len(arg) == 3:
                raise ArgsParsingError(
                    f'Incorrect flag usage: "{arg}" should have been "{arg[1:]}"'
                )
            new_flag = arg[2:]
        elif arg.startswith("-"):
            if len(arg) == 1:
                raise ArgsParsingError(f'Incorrect flag usage: "-" lacks flag name')
            if len(arg) > 2:
                raise ArgsParsingError(
                    f'Incorrect flag usage: "{arg}" should have been "-{arg}"'
                )
            new_flag = arg[1]

        # If it is just a quote, raise - quoted args should be trimmed.
        elif arg == '"':
            raise ArgsParsingError("Parsing error: lone quote")  # todo test this

        # If it starts with a quote, begin parsing a quoted arg.
        elif arg.startswith('"'):
            # If a quoted arg is already being parsed and this does not just close it.
            if current_arg is not None:
                raise ArgsParsingError(
                    "Parsing error: new quote opened before closing the last"
                )
            else:
                # Empty string arg.
                if arg == '""':
                    arg = ""
                # Begin a quoted arg.
                else:
                    current_arg = arg[1:]
                    continue

        # If it ends with a quote, finish parsing a quoted arg.
        elif arg.endswith('"') and not arg.endswith('\\"'):
            if current_arg is None:
                raise ArgsParsingError("Parsing error: unpaired closing quote")
            current_arg += f" {arg[:-1]}"
            arg = current_arg
            current_arg = None

        # If it's already processing a quoted arg, append the value.
        elif current_arg is not None:
            # The only empty string is the one appended at the beginning.
            if len(arg):
                current_arg += f" {arg}"
                continue
            else:
                raise ArgsParsingError("Parsing error: unclosed quote")  # todo test me

        # If it's not empty, it's a regular unquoted arg.
        elif len(arg):
            pass

        # End reached; exit the loop.
        else:
            break

        # If it was a quoted arg, remove quotes.
        if arg.startswith('"') and arg.endswith('"'):
            arg = arg[1:-1]

        # Unescaped quotes should only be used to enclose a quoted arg.
        if '"' in arg and len(arg.split('"')) != len(arg.split('\\"')):
            raise ArgsParsingError("Parsing error: incorrect quote usage")

        # Unescape quotes.
        arg = arg.replace('\\"', '"')

        # If it's a new flag, add it to the dictionary.
        if new_flag:
            flags_and_kwargs[new_flag] = []
            current_flag = new_flag
        else:
            # If it's still processing args, add it to the list.
            if current_flag is None:
                args.append(arg)
            # Otherwise, add it to the current kwarg.
            else:
                flags_and_kwargs[current_flag].append(arg)

    # Split kwargs from flags.
    kwargs = {}
    flags = []
    for key, value in flags_and_kwargs.items():
        if len(value):
            kwargs[key] = value
        else:
            flags.append(key)

    return ArgsDict(args, kwargs, flags)
