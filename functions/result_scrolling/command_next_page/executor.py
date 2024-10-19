from functions.commands.definition.ActionEnum import ActionEnum
from functions.commands.definition.ArgsDict import ArgsDict
from functions.execute.result.ExecutionResult import ExecutionResult

from functions.result_scrolling.current_position import current_position


def next_page(args_dict: ArgsDict) -> ExecutionResult:
    current_position.update()
    if current_position.total_pages == 0:
        return ExecutionResult.error_message("No result to paginate.")
    if current_position.page_number == current_position.total_pages - 1:
        return ExecutionResult.error_message("This is the last page.")
    if current_position.page_number > current_position.total_pages - 1:
        current_position.page_number = current_position.total_pages - 2
    current_position.page_number += 1
    return ExecutionResult.action(ActionEnum.Refresh)
