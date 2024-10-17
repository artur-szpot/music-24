from typing import Callable, List, Dict

from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import (
    FunctionDefinition,
    MusicFunction,
)
from functions.data_types.DataType import DataType
from functions.data_types.DataTypeEnum import DataTypeEnum
from functions.data_types.DataTypeRegistry import DataTypeRegistry
from functions.data_types.artist_registry import artist_registry
from functions.data_types.genre_registry import genre_registry
from functions.execute.ArgsValidator import ArgsValidator
from functions.execute.ExecutionResult import ExecutionResult
from libs.error_handling import error_message_to_string
from libs.strings import indefinite


def add_variant_definition(data_type: DataTypeEnum, alias: bool) -> FunctionDefinition:
    constructor: Callable[[str, List[str], List[str], Dict[str, str]], DataType]
    registry: DataTypeRegistry
    variant_name = 'alias' if alias else 'misspelling'
    if data_type == DataTypeEnum.ARTIST:
        registry = artist_registry
    else:
        registry = genre_registry
    return FunctionDefinition(
        function=add_variant(registry, alias),
        verbs=[f"add-{data_type.value}-{variant_name}", f"add-{variant_name}-{data_type.value}",f"{data_type.value}-{variant_name}", f"{variant_name}-{data_type.value}"],
        args_validator=ArgsValidator.args(exact=2),
        description=f"Add a new {variant_name} for {indefinite(data_type.value)} in the database.",
        category=FunctionCategoryEnum.DataTypeManagement,
    )


def add_variant(
        registry: DataTypeRegistry,
        alias: bool
) -> MusicFunction:
    def add_variant_typed(args_dict: ArgsDict) -> ExecutionResult:
        name = args_dict.get_arg(0)
        variant = args_dict.get_arg(1)
        try:
            registry.add_variant(name, variant, alias)
        except Exception as e:
            return ExecutionResult.error_message(error_message_to_string(e))
        return ExecutionResult.refresh()

    return add_variant_typed
