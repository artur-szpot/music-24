from typing import Dict, List, Callable, Optional, NewType

from functions.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.definition.ArgsDict import ArgsDict
from functions.execute.ArgsValidator import ArgsValidator
from functions.execute.ExecutionResult import ExecutionResult

MusicFunction = Callable[[ArgsDict], ExecutionResult]


class ParameterHelp:
    description: str
    types: str

    def __init__(self, description: str, types: str):
        self.description = description
        self.types = types


class FunctionDefinition:
    description: str
    function: MusicFunction
    category: FunctionCategoryEnum
    parameters: Dict[str, ParameterHelp]
    verbs: List[str]
    args_validator: ArgsValidator

    def __init__(
        self,
        function: MusicFunction,
        verbs: List[str],
        description: str,
        category: FunctionCategoryEnum,
        parameters: Dict[str, ParameterHelp] = None,
        args_validator: ArgsValidator = ArgsValidator.no_args(),
    ):
        self.function = function
        self.verbs = verbs
        self.description = description
        self.category = category
        self.parameters = parameters
        self.args_validator = args_validator
