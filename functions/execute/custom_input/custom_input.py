from typing import List

from readchar import readkey, key
from termcolor import cprint

from functions.settings.app_settings import app_settings
from functions.settings.text_color.SchemeColor import SchemeColor

ALLOWED_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz01234567890-\"',./?\\|;:[]{}_+=!@#$%^&*()<>"


def custom_input(memory: List[str]) -> str:
    current_input = ""
    cursor_position = 0
    history_position = 0
    text_color = app_settings.color_mapper(SchemeColor.BASE).value
    previous_length = 1
    while True:
        # print the input and cover up potential history
        cprint(
            "\r" + ">_ " + current_input,
            end=" " * (previous_length - len(current_input)),
            color=text_color,
        )
        # print again to set the cursor in the right position
        cprint("\r" + ">_ " + current_input[:cursor_position], end="", color=text_color)
        # save the current input length for next round cover-up
        previous_length = len(current_input)

        k = readkey()
        if k in ALLOWED_CHARS:
            current_input = (
                current_input[:cursor_position] + k + current_input[cursor_position:]
            )
            cursor_position += 1
        if k == " ":
            current_input = (
                current_input[:cursor_position] + k + current_input[cursor_position:]
            )
            cursor_position += 1
            if current_input == " ":
                print("\r")
                return current_input
        if k == key.TAB:
            if len(current_input) > 0:
                # todo some kind of input completion?
                pass
            print("\r")
            return "\t"
        elif k == key.ENTER:
            print("\r")
            return current_input
        elif k == key.BACKSPACE:
            if cursor_position > 0:
                current_input = (
                    current_input[: cursor_position - 1]
                    + current_input[cursor_position:]
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
        # elif k == key.ESC:
        #     raise KeyError()
        elif k == key.UP:
            history_position = min(len(memory), history_position + 1)
            current_input = memory[-history_position]
            cursor_position = len(current_input)
        elif k == key.DOWN:
            history_position = max(0, history_position - 1)
            if history_position == 0:
                current_input = ""
            else:
                current_input = memory[-history_position]
            cursor_position = len(current_input)
        # else:
        #     print(k)
