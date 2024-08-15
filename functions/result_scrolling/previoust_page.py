from functions.definition.ActionEnum import ActionEnum
from functions.definition.ArgsDict import ArgsDict
from functions.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ArgsExtractor import ArgsExtractor
from functions.execute.ExecutionResult import ExecutionResult

from functions.result_scrolling.current_position import current_position


def previous_page_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=previous_page,
        verbs=["previous-page", "previous", "pp"],
        description="Move to the previous page of the results",
        category=FunctionCategoryEnum.ViewingFiles,
        returns_result=False,
    )


def previous_page(args_dict: ArgsDict) -> ExecutionResult:
    ArgsExtractor.no_args(args_dict)
    if current_position.total_pages == 0:
        return ExecutionResult(
            error_message="No result to paginate.", action=ActionEnum.Refresh
        )
    if current_position.page_number == 0:
        return ExecutionResult(
            error_message="This is the first page.",
            action=ActionEnum.Refresh,
        )
    current_position.page_number -= 1
    return ExecutionResult.action(ActionEnum.Refresh)
