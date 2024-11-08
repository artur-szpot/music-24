from typing import Callable, List, Dict

from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import (
    FunctionDefinition,
)
from functions.data_types.DataType import DataType
from functions.data_types.DataTypeEnum import DataTypeEnum
from functions.data_types.DataTypeRegistry import DataTypeRegistry
from functions.data_types.artist_registry import artist_registry
from functions.data_types.functions.command_add_variant.verbs import add_variant_verbs
from functions.data_types.functions.command_add_variant.executor import add_variant
from functions.data_types.genre_registry import genre_registry
from functions.execute.validate.ArgsValidator import ArgsValidator
from libs.strings import indefinite


def add_variant_definition(data_type: DataTypeEnum, alias: bool) -> FunctionDefinition:
    constructor: Callable[[str, List[str], List[str], Dict[str, str]], DataType]
    registry: DataTypeRegistry
    variant_name = "alias" if alias else "misspelling"
    if data_type == DataTypeEnum.ARTIST:
        registry = artist_registry
    else:
        registry = genre_registry
    return FunctionDefinition(
        function=add_variant(registry, alias),
        verbs=add_variant_verbs(data_type, variant_name),
        args_validator=ArgsValidator.args(exact=2),
        description=f"Add a new {variant_name} for {indefinite(data_type.value)} in the database.",
        category=FunctionCategoryEnum.DataTypeManagement,
    )
