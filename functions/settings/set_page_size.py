from functions.definition.ActionEnum import ActionEnum
from functions.definition.ArgsDict import ArgsDict
from functions.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ArgsExtractor import ArgsExtractor
from functions.execute.ExecutionResult import ExecutionResult

from functions.result_scrolling.current_position import current_position
from functions.settings.app_settings import app_settings


def set_page_size_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=set_page_size,
        verbs=["page-size", "ps"],
        description="Set the number of results to appear on a page",
        category=FunctionCategoryEnum.AppSettings,
        returns_result=False,
    )


def set_page_size(args_dict: ArgsDict) -> ExecutionResult:
    page_size = int(ArgsExtractor.single_arg(args_dict))
    if app_settings.page_size == page_size:
        return ExecutionResult(
            error_message=f"Page size was already set to {page_size}.",
            action=ActionEnum.Refresh,
        )
    if page_size < 1 or page_size > 100:
        return ExecutionResult(
            error_message=f"Wrong page size: {page_size}. Use a value between 1 and 100.",
            action=ActionEnum.Refresh,
        )
    current_position.set_page_size(page_size)
    return ExecutionResult.action(ActionEnum.Refresh)
