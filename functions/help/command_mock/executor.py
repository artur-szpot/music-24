from functions.commands.definition.ArgsDict import ArgsDict
from functions.execute.result.ExecutionResult import ExecutionResult


def mock_function(args_dict: ArgsDict) -> ExecutionResult:
    return ExecutionResult.refresh()
