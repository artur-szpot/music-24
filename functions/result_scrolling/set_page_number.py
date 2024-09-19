from functions.commands.definition.ActionEnum import ActionEnum
from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ArgsValidator import ArgsValidator
from functions.execute.ExecutionResult import ExecutionResult

from functions.result_scrolling.current_position import current_position


def set_page_number_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=set_page_number,
        verbs=["page", "p"],
        args_validator=ArgsValidator.args(exact=1),
        description="Move to a given page of the results",
        category=FunctionCategoryEnum.ViewingFiles,
    )


def set_page_number(args_dict: ArgsDict) -> ExecutionResult:
    page_number = int(args_dict.get_arg())
    if current_position.total_pages == 0:
        return ExecutionResult(
            error_message="No result to paginate.", action=ActionEnum.Refresh
        )
    if page_number < 1 or page_number > current_position.total_pages:
        return ExecutionResult(
            error_message=f"Wrong page number: {page_number}. Use a value between 1 and {current_position.total_pages}.",
            action=ActionEnum.Refresh,
        )
    current_position.page_number = page_number - 1
    return ExecutionResult.action(ActionEnum.Refresh)
