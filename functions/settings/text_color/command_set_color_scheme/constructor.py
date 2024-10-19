from functions.commands.print_command import print_command
from functions.settings.text_color.ColorScheme import ColorScheme
from functions.settings.text_color.command_set_color_scheme.definition import (
    set_color_scheme_definition,
)


class SetColorSchemeCommand:
    @staticmethod
    def create(color_scheme: ColorScheme) -> str:
        return print_command(set_color_scheme_definition(), args=[color_scheme.value])
