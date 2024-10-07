import os
from typing import List

from constants.debug import debug_tools
from functions.commands.CommandEnum import CommandEnum
from functions.commands.definition.ActionEnum import ActionEnum
from functions.execute.ExecutionResult import ExecutionResultCategory
from functions.execute.FullExecutionResult import FullExecutionResult
from functions.execute.custom_input import custom_input
from functions.execute.execute import execute_command, DisallowedCommandError
from functions.lines.Line import Line
from functions.query_cache.query_cache import query_cache
from functions.result_scrolling.CurrentPosition import HeaderType, TerminalSizeError
from functions.result_scrolling.current_position import current_position
from libs.error_handling import error_message_to_string


def clear():
    if not debug_tools.pause_screen_cleaning:
        os.system("cls")


display: FullExecutionResult = FullExecutionResult()
memory = {"action": ActionEnum.Refresh}


def terminal_size_fault_loop(
    terminal_size_message: str, other_message: str = None
) -> None:
    clear()
    Line.simple(terminal_size_message).render(current_position.max_width)
    if other_message:
        Line.simple(other_message).render(current_position.max_width)
    command = custom_input()
    try:
        new_result = execute_command(
            command, [CommandEnum.SetPageSize, CommandEnum.Exit]
        )
        if new_result.result is not None:
            memory["action"] = new_result.result.get_action()
    except DisallowedCommandError as error:
        terminal_size_fault_loop(terminal_size_message, error_message_to_string(error))
    except TerminalSizeError as error:
        terminal_size_fault_loop(error_message_to_string(error))


def main_loop(
    last_command: str = None, message: List[Line] = None, initial_check: bool = False
) -> None:
    clear()
    if message:
        for line in message:
            line.render(current_position.max_width)
        print()
    if not initial_check:
        command = custom_input()
    else:
        command = ""
    try:
        if initial_check:
            current_position.update()
            main_loop()
        else:
            normal_loop(command, last_command)
    except TerminalSizeError as error:
        terminal_size_fault_loop(error_message_to_string(error))
        while 1:
            try:
                normal_loop_finisher(command, last_command)
                break
            except TerminalSizeError as error:
                terminal_size_fault_loop(error_message_to_string(error))


def normal_loop(command: str, last_command: str = None) -> None:
    if not len(command):
        previous_result = query_cache.get("last")
        if previous_result is not None and previous_result.default_command:
            command = previous_result.default_command
        else:
            normal_loop_finisher(command, last_command)

    new_result: FullExecutionResult = execute_command(command)
    if new_result.result is not None:
        memory["action"] = new_result.result.get_action()
        if new_result.result.category == ExecutionResultCategory.Query:
            query_cache["last"] = new_result.result
            current_position.new_result(
                new_result.result.get_total_items(), HeaderType.TABLE_HEADER
            )
            display.result = new_result.result
            display.message = None
        elif new_result.result.category == ExecutionResultCategory.Detail:
            current_position.new_result(
                new_result.result.get_total_items(), HeaderType.SIMPLE_PAGINATION
            )
            display.result = new_result.result
            display.message = None
        elif new_result.result.category in [
            ExecutionResultCategory.Message,
            ExecutionResultCategory.Action,
        ]:
            display.message = new_result.result.get_message()
    if not display.message or display.message.is_empty():
        display.message = Line.simple(f">_ {last_command}" if last_command else "")
    normal_loop_finisher(command, last_command)


def normal_loop_finisher(command: str, last_command: str = None):
    action = memory["action"]
    if action == ActionEnum.Return:
        clear()
        return
    render = display.render(current_position)
    if action == ActionEnum.Repeat:
        # shows the command used, aka query
        main_loop(last_command=command, message=render)
    elif action == ActionEnum.Refresh:
        # doesn't show the new command to keep the query visible
        main_loop(last_command=last_command, message=render)
    else:
        main_loop(last_command=f"Unhandled action: {action.value}")


if __name__ == "__main__":
    main_loop(initial_check=True)
