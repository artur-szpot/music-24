from functions.definition.ActionEnum import ActionEnum
from functions.definition.ArgsDict import ArgsDict
from functions.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ArgsValidator import ArgsValidator
from functions.execute.ExecutionResult import ExecutionResult

from functions.result_scrolling.current_position import current_position


def next_page_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=next_page,
        verbs=["next-page", "next", "np"],
        args_validator=ArgsValidator.no_args(),
        description="Move to the next page of the results",
        category=FunctionCategoryEnum.ViewingFiles,
    )


def next_page(args_dict: ArgsDict) -> ExecutionResult:
    if current_position.total_pages == 0:
        return ExecutionResult(
            error_message="No result to paginate.", action=ActionEnum.Refresh
        )
    if current_position.page_number == current_position.total_pages - 1:
        return ExecutionResult(
            error_message="This is the last page.",
            action=ActionEnum.Refresh,
        )
    current_position.page_number += 1
    return ExecutionResult.action(ActionEnum.Refresh)
