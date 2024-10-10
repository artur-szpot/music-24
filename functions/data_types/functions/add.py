from typing import Callable, List, Dict

from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import (
    FunctionDefinition,
    MusicFunction,
)
from functions.data_types.Artist import Artist
from functions.data_types.DataType import DataType
from functions.data_types.DataTypeEnum import DataTypeEnum
from functions.data_types.DataTypeRegistry import DataTypeRegistry
from functions.data_types.Genre import Genre
from functions.data_types.artist_registry import artist_registry
from functions.data_types.genre_registry import genre_registry
from functions.execute.ArgsValidator import ArgsValidator
from functions.execute.ExecutionResult import ExecutionResult
from functions.execute.validate_args import AllowedKwarg


def add_definition(data_type: DataTypeEnum) -> FunctionDefinition:
    constructor: Callable[[str, List[str], List[str], Dict[str, str]], DataType]
    registry: DataTypeRegistry
    additional_kwargs = []
    required_kwargs = []
    if data_type == DataTypeEnum.ARTIST:
        registry = artist_registry
        constructor = Artist.create
    else:
        registry = genre_registry
        constructor = Genre.create
        required_kwargs = [AllowedKwarg.single(["category", "cat", "c"])]
    return FunctionDefinition(
        function=add(registry, constructor),
        verbs=[f"add-{data_type.value}"],
        args_validator=ArgsValidator.args(exact=1).kwargs(
            allowed_kwargs=[
                AllowedKwarg.any(["aliases", "alias", "a"]),
                AllowedKwarg.any(["misspellings", "miss", "m"]),
            ],
            required_kwargs=required_kwargs,
        ),
        description=f"Add a new {data_type.value} to the database.",
        category=FunctionCategoryEnum.DataTypeManagement,
    )


def add(
    registry: DataTypeRegistry,
    constructor: Callable[[str, List[str], List[str], Dict[str, str]], DataType],
) -> MusicFunction:
    def add_typed(args_dict: ArgsDict) -> ExecutionResult:
        name = args_dict.get_arg(0)
        aliases = args_dict.get_kwarg("aliases")
        misspellings = args_dict.get_kwarg("misspellings")
        category_raw = args_dict.get_kwarg("category")
        category = None
        if category_raw is not None and len(category_raw):
            category = category_raw[0]
        other = {}
        if category is not None:
            other["category"] = category
        registry.add(constructor(name, aliases, misspellings, other))
        return ExecutionResult.refresh()

    return add_typed
