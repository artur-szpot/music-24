from typing import List

from functions.commands.command_registry import command_registry
from functions.definition.ArgsDict import ArgsDict
from functions.execute.execute import ExecutionResult
from functions.help.help_definition import help_definition


def parse_args(input_command) -> ArgsDict:
    input_parts = input_command.split(" ")
    command = input_parts[0]
    args_raw = input_parts[1:]
    args = parse_args_exe(args_raw)
    if command in help_definition().verbs:
        args.system = {"command_registry": command_registry}
    return args


def parse_args_exe(args_raw: List[str]) -> ArgsDict:
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
