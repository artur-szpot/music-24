from functions.cache import cache
from functions.commands.definition.ArgsDict import ArgsDict
from functions.execute.result.ExecutionResult import ExecutionResult
from functions.lines.Line import Line


def show_log(args_dict: ArgsDict) -> ExecutionResult:
    return ExecutionResult.paginable(
        header=[Line.simple("Last logs")],
        items=[Line.simple(log) for log in cache.get_command_log()],
    )
