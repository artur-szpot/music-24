import os

from enums.results import ResultEnum
from execute.execute import execute_command


def clear():
    os.system('cls')


def main_loop(message=None):
    clear()
    if message:
        print(message)
        print()
    command = input('>_ ')
    result, message = execute_command(command)
    if result == ResultEnum.Return:
        clear()
        return
    elif result == ResultEnum.Repeat:
        main_loop(message)
    else:
        main_loop(f'Unknown result: {result}')


if __name__ == '__main__':
    main_loop()
