from functions.commands.definition.ActionEnum import ActionEnum
from functions.commands.definition.ArgsDict import ArgsDict
from functions.execute.result.ExecutionResult import (
    ExecutionResult,
    ExecutionResultCategory,
)
from functions.lines.Line import Line

from functions.result_scrolling.current_position import current_position
from functions.settings.AppSettings import PAGE_SIZE_AUTO
from functions.settings.app_settings import app_settings
from functions.settings.text_color.command_set_page_size.flags import (
    set_page_size_flags,
    SetPageSizeFlags,
)


def set_page_size(args_dict: ArgsDict) -> ExecutionResult:
    arg = args_dict.get_arg()
    auto = args_dict.has_flag(set_page_size_flags[SetPageSizeFlags.Auto])
    if arg is None and not auto:
        return ExecutionResult(
            message=Line.simple(
                f"Page size is set to {app_settings.page_size_string()}."
            ),
            action=ActionEnum.Refresh,
            category=ExecutionResultCategory.Message,
        )
    elif arg is not None and auto:
        return ExecutionResult(
            message=Line.simple(
                "Page size cannot be defined and set automatically at the same time."
            ),
            action=ActionEnum.Refresh,
            category=ExecutionResultCategory.Message,
        )
    elif auto:
        page_size = PAGE_SIZE_AUTO
    else:
        page_size = int(arg)
    if app_settings.page_size == page_size:
        if auto:
            return ExecutionResult(
                message=Line.simple(f"Page size was already set to automatic."),
                action=ActionEnum.Refresh,
                category=ExecutionResultCategory.Message,
            )
        return ExecutionResult(
            message=Line.simple(f"Page size was already set to {page_size}."),
            action=ActionEnum.Refresh,
            category=ExecutionResultCategory.Message,
        )
    if not auto and (page_size < 1 or page_size > 100):
        return ExecutionResult(
            message=Line.simple(
                f"Wrong page size: {page_size}. Use a value between 1 and 100."
            ),
            action=ActionEnum.Refresh,
            category=ExecutionResultCategory.Message,
        )
    current_position.set_page_size(page_size)
    return ExecutionResult.action(ActionEnum.Refresh)
