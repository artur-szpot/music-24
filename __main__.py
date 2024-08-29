import os
from typing import Dict, List
from termcolor import cprint

from constants.debug import debug_tools
from functions.definition.ActionEnum import ActionEnum
from functions.execute.ExecutionResult import ExecutionResult, ExecutionResultCategory
from functions.execute.FullExecutionResult import FullExecutionResult
from functions.execute.Line import Line
from functions.execute.execute import execute_command
from functions.query_cache.query_cache import query_cache
from functions.result_scrolling.current_position import current_position


def clear():
    if not debug_tools.pause_screen_cleaning:
        os.system("cls")


display: FullExecutionResult = FullExecutionResult()


def main_loop(last_command: str = None, message: List[Line] = None):
    clear()
    if last_command:
        print(f">_ {last_command}")
        print()
    if message:
        for line in message:
            line.render()
        print()
    command = input(">_ ")
    new_result: FullExecutionResult = execute_command(command)
    if new_result.result is not None:
        if new_result.result.category == ExecutionResultCategory.Query:
            query_cache["last"] = new_result.result
            current_position.new_result(new_result.result.get_total_items())
            display.result = new_result.result
        elif new_result.result.category == ExecutionResultCategory.Detail:
            current_position.new_result(new_result.result.get_total_items())
            display.result = new_result.result
        elif new_result.result.category == ExecutionResultCategory.Message:
            display.message = new_result.result.get_message()
    # result = query_cache.get("last") or new_result.result
    # error_message=None
    # if new_result.result:
    #     error_message = new_result.result.get_error_message()
    render = display.render(current_position)
    action = new_result.result.action
    if action == ActionEnum.Return:
        clear()
        return
    elif action == ActionEnum.Repeat:
        main_loop(last_command=command, message=render)
    elif action == ActionEnum.Refresh:
        main_loop(last_command=last_command, message=render)
    else:
        main_loop(last_command=f"Unhandled action: {action.value}")


if __name__ == "__main__":
    main_loop()
