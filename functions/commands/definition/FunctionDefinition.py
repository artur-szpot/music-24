from typing import Dict, List, Callable, Optional

from functions.commands.CommandEnum import CommandEnum
from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
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
    command: CommandEnum
    default_command: Optional[str]

    def __init__(
        self,
        function: MusicFunction,
        verbs: List[str],
        description: str,
        category: FunctionCategoryEnum,
        parameters: Dict[str, ParameterHelp] = None,
        args_validator: ArgsValidator = ArgsValidator.no_args(),
        default_command: str = None,
    ):
        self.function = function
        self.verbs = verbs
        self.description = description
        self.category = category
        self.parameters = parameters
        self.args_validator = args_validator
        self.command = CommandEnum.Exit
        self.default_command = default_command

    def with_command(self, command: CommandEnum):
        self.command = command
        return self
