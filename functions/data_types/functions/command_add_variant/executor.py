from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionDefinition import (
    MusicFunction,
)
from functions.data_types.DataTypeRegistry import DataTypeRegistry
from functions.execute.result.ExecutionResult import ExecutionResult
from libs.error_handling import error_message_to_string


def add_variant(registry: DataTypeRegistry, alias: bool) -> MusicFunction:
    def add_variant_typed(args_dict: ArgsDict) -> ExecutionResult:
        name = args_dict.get_arg(0)
        variant = args_dict.get_arg(1)
        try:
            registry.add_variant(name, variant, alias)
        except Exception as e:
            return ExecutionResult.error_message(error_message_to_string(e))
        return ExecutionResult.refresh()

    return add_variant_typed
