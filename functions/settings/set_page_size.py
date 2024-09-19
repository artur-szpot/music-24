from functions.commands.definition.ActionEnum import ActionEnum
from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ArgsValidator import ArgsValidator
from functions.execute.ExecutionResult import ExecutionResult, ExecutionResultCategory
from functions.lines.Line import Line

from functions.result_scrolling.current_position import current_position
from functions.settings.app_settings import app_settings


def set_page_size_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=set_page_size,
        verbs=["page-size", "ps"],
        args_validator=ArgsValidator.args(max=1),
        description="Check or set the number of results to appear on a page",
        category=FunctionCategoryEnum.AppSettings,
    )


def set_page_size(args_dict: ArgsDict) -> ExecutionResult:
    arg = args_dict.get_arg()
    if arg is None:
        return ExecutionResult(
            message=Line.simple(f"Page size is set to {app_settings.page_size}."),
            action=ActionEnum.Refresh,
            category=ExecutionResultCategory.Message,
        )
    else:
        page_size = int(arg)
    if app_settings.page_size == page_size:
        return ExecutionResult(
            message=Line.simple(f"Page size was already set to {page_size}."),
            action=ActionEnum.Refresh,
            category=ExecutionResultCategory.Message,
        )
    if page_size < 1 or page_size > 100:
        return ExecutionResult(
            message=Line.simple(
                f"Wrong page size: {page_size}. Use a value between 1 and 100."
            ),
            action=ActionEnum.Refresh,
            category=ExecutionResultCategory.Message,
        )
    current_position.set_page_size(page_size)
    return ExecutionResult.action(ActionEnum.Refresh)
