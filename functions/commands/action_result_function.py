from functions.commands.definition import ActionEnum
from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionDefinition import MusicFunction
from functions.execute.ExecutionResult import ExecutionResult


def action_result_function(action: ActionEnum) -> MusicFunction:
    def constructed_function(args_dict: ArgsDict) -> ExecutionResult:
        return ExecutionResult.action(action)

    return constructed_function
