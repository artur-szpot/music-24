from functions.cache import cache
from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ArgsValidator import ArgsValidator
from functions.execute.ExecutionResult import ExecutionResult
from functions.lines.Line import Line


def show_log_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=show_log,
        verbs=["show-log", "log"],
        args_validator=ArgsValidator.no_args(),
        description="Shows the last few executed commands.",
        category=FunctionCategoryEnum.AppManagement,
    )


def show_log(args_dict: ArgsDict) -> ExecutionResult:
    return ExecutionResult.paginable(
        header=[Line.simple("Last logs")],
        items=[Line.simple(log) for log in cache.get_command_log()],
    )
