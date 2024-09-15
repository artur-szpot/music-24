import os
from typing import List

from termcolor import cprint

from constants.debug import debug_tools
from functions.definition.ActionEnum import ActionEnum
from functions.execute.ExecutionResult import ExecutionResultCategory
from functions.execute.FullExecutionResult import FullExecutionResult
from functions.execute.execute import execute_command
from functions.lines.Line import Line
from functions.query_cache.query_cache import query_cache
from functions.result_scrolling.CurrentPosition import HeaderType
from functions.result_scrolling.current_position import current_position

from readchar import readkey, key, readchar


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
            line.render(current_position.max_width)
        print()
    command = test_inputs()  # (">_ ")
    new_result: FullExecutionResult = execute_command(command)
    if new_result.result is not None:
        if new_result.result.category == ExecutionResultCategory.Query:
            query_cache["last"] = new_result.result
            current_position.new_result(new_result.result.get_total_items(), HeaderType.TABLE_HEADER)
            display.result = new_result.result
            display.message = None
        elif new_result.result.category == ExecutionResultCategory.Detail:
            current_position.new_result(new_result.result.get_total_items(), HeaderType.SIMPLE_PAGINATION)
            display.result = new_result.result
            display.message = None
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


def test_inputs() -> str:
    current_input = ""
    cursor_position = 0
    while True:
        cprint("\r" + ">_ " + current_input, end=" ", color="black")
        cprint("\r" + ">_ " + current_input[:cursor_position], end="", color="black")
        k = readkey()
        if (
            k
            in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890 -\"',./?\\|;:[]{}_+=!@#$%^&*()<>"
        ):
            current_input = (
                current_input[:cursor_position] + k + current_input[cursor_position:]
            )
            cursor_position += 1
        elif k == key.ENTER:
            print("\r")
            return current_input
        elif k == key.BACKSPACE:
            current_input = (
                current_input[: cursor_position - 1] + current_input[cursor_position:]
            )
            cursor_position -= 1
        elif k == key.DELETE:
            current_input = (
                current_input[:cursor_position] + current_input[cursor_position + 1 :]
            )
        elif k == key.LEFT:
            cursor_position = max(cursor_position - 1, 0)
        elif k == key.RIGHT:
            cursor_position = min(cursor_position + 1, len(current_input))
        elif k == key.HOME:
            cursor_position = 0
        elif k == key.END:
            cursor_position = len(current_input)
        elif k == key.PAGE_UP:
            if cursor_position > 0:
                cursor_position -= 1
                while current_input[cursor_position] == " " and cursor_position > 0:
                    cursor_position -= 1
                while current_input[cursor_position - 1] != " " and cursor_position > 0:
                    cursor_position -= 1
        elif k == key.PAGE_DOWN:
            if cursor_position < len(current_input):
                fake_current_input = current_input + " "
                cursor_position += 1
                while fake_current_input[
                    cursor_position
                ] == " " and cursor_position < len(current_input):
                    cursor_position += 1
                while fake_current_input[
                    cursor_position
                ] != " " and cursor_position < len(current_input):
                    cursor_position += 1
        elif k == key.ESC:
            raise KeyError()
        # else:
        #     print(k)


if __name__ == "__main__":
    main_loop()
