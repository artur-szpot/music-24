from readchar import readkey, key
from termcolor import cprint

from functions.settings.app_settings import app_settings
from functions.settings.text_color.SchemeColor import SchemeColor


def custom_input() -> str:
    current_input = ""
    cursor_position = 0
    text_color = app_settings.color_mapper(SchemeColor.BASE).value
    while True:
        cprint("\r" + ">_ " + current_input, end=" ", color=text_color)
        cprint("\r" + ">_ " + current_input[:cursor_position], end="", color=text_color)
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
