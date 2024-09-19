from functions.commands.definition.ActionEnum import ActionEnum
from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ArgsValidator import ArgsValidator
from functions.execute.ExecutionResult import ExecutionResult

from functions.result_scrolling.current_position import current_position


def previous_page_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=previous_page,
        verbs=["previous-page", "previous", "pp"],
        args_validator=ArgsValidator.no_args(),
        description="Move to the previous page of the results",
        category=FunctionCategoryEnum.ViewingFiles,
    )


def previous_page(args_dict: ArgsDict) -> ExecutionResult:
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
