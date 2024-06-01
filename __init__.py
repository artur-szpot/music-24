import os

from constants.debug import debug_tools
from enums.results import ResultEnum
from functions.execute.execute import execute_command


def clear():
    if not debug_tools.pause_screen_cleaning:
        os.system("cls")


def main_loop(last_command=None, message=None):
    clear()
    if last_command:
        print(f">_ {last_command}")
        print()
    if message:
        for line in message:
            print(line)
        print()
    command = input(">_ ")
    result = execute_command(command)
    if result.action == ResultEnum.Return:
        clear()
        return
    elif result.action == ResultEnum.Repeat:
        main_loop(command, result.message)
    else:
        main_loop(f"Unknown result: {result}")


if __name__ == "__main__":
    main_loop()
