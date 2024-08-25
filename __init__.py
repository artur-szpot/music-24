import os
from typing import Dict, List
from termcolor import cprint

from constants.debug import debug_tools
from functions.definition.ActionEnum import ActionEnum
from functions.execute.ExecutionResult import ExecutionResult
from functions.execute.FullExecutionResult import FullExecutionResult
from functions.execute.Line import Line
from functions.execute.execute import execute_command
from functions.result_cache.result_cache import result_cache
from functions.result_scrolling.current_position import current_position


def clear():
    if not debug_tools.pause_screen_cleaning:
        os.system("cls")


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
    if new_result.command is not None and new_result.command.returns_result:
        result_cache["last"] = new_result.result
        current_position.new_result(new_result.result.get_total_items())
    result = result_cache.get("last") or new_result.result
    error_message=None
    if new_result.result:
        error_message = new_result.result.get_error_message()
    render = result.render(current_position, error_message)
    action = new_result.result.get_action()
    if action == ActionEnum.Return:
        clear()
        return
    elif action == ActionEnum.Repeat:
        main_loop(last_command=command, message=render)
    elif action == ActionEnum.Refresh:
        main_loop(last_command=last_command, message=render)
    else:
        main_loop(last_command=f"Unknown result: {result}")


if __name__ == "__main__":
    main_loop()
