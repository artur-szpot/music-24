from typing import Callable, List, Dict

from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionDefinition import (
    MusicFunction,
)
from functions.data_types.DataType import DataType
from functions.data_types.DataTypeRegistry import DataTypeRegistry
from functions.data_types.functions.command_add.kwargs import AddKwargs
from functions.execute.result.ExecutionResult import ExecutionResult
from libs.error_handling import error_message_to_string


def add(
    registry: DataTypeRegistry,
    constructor: Callable[[str, List[str], List[str], Dict[str, str]], DataType],
) -> MusicFunction:
    def add_typed(args_dict: ArgsDict) -> ExecutionResult:
        name = args_dict.get_arg(0)
        aliases = args_dict.get_kwarg(AddKwargs.Aliases)
        misspellings = args_dict.get_kwarg(AddKwargs.Misspellings)

        category_raw = args_dict.get_kwarg(AddKwargs.Category)
        category = None
        if category_raw is not None and len(category_raw):
            category = category_raw[0]

        other = {}
        if category is not None:
            other["category"] = category

        try:
            registry.add(constructor(name, aliases, misspellings, other))
        except Exception as e:
            return ExecutionResult.error_message(error_message_to_string(e))
        return ExecutionResult.refresh()

    return add_typed
