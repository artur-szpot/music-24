from typing import Callable, List, Dict

from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import (
    FunctionDefinition,
)
from functions.data_types.Artist import Artist
from functions.data_types.DataType import DataType
from functions.data_types.DataTypeEnum import DataTypeEnum
from functions.data_types.DataTypeRegistry import DataTypeRegistry
from functions.data_types.Genre import Genre
from functions.data_types.artist_registry import artist_registry
from functions.data_types.functions.command_add.executor import add
from functions.data_types.functions.command_add.kwargs import AddKwargs, add_kwargs
from functions.data_types.functions.command_add.verbs import add_verbs
from functions.data_types.genre_registry import genre_registry
from functions.execute.validate.ArgsValidator import ArgsValidator
from functions.execute.validate.validate_args import KwargDefinition


def add_definition(data_type: DataTypeEnum) -> FunctionDefinition:
    constructor: Callable[[str, List[str], List[str], Dict[str, str]], DataType]
    registry: DataTypeRegistry
    required_kwargs = []
    if data_type == DataTypeEnum.ARTIST:
        registry = artist_registry
        constructor = Artist.create
    else:
        registry = genre_registry
        constructor = Genre.create
        required_kwargs = [KwargDefinition.single(add_kwargs(AddKwargs.Category))]
    return FunctionDefinition(
        function=add(registry, constructor),
        verbs=add_verbs(data_type),
        args_validator=ArgsValidator.args(exact=1).kwargs(
            allowed_kwargs=[
                KwargDefinition.any(add_kwargs(AddKwargs.Aliases)),
                KwargDefinition.any(add_kwargs(AddKwargs.Misspellings)),
            ],
            required_kwargs=required_kwargs,
        ),
        description=f"Add a new {data_type.value} to the database.",
        category=FunctionCategoryEnum.DataTypeManagement,
    )
