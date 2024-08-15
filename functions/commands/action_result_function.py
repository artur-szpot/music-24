from functions.definition import ActionEnum
from functions.definition.ArgsDict import ArgsDict
from functions.definition.FunctionDefinition import MusicFunction
from functions.execute.ExecutionResult import ExecutionResult
from functions.execute.ArgsExtractor import ArgsExtractor


def action_result_function(action: ActionEnum) -> MusicFunction:
    def constructed_function(args_dict: ArgsDict) -> ExecutionResult:
        ArgsExtractor.no_args(args_dict)
        return ExecutionResult.action(action)

    return constructed_function
