from functions.commands.print_command import print_command
from functions.settings.text_color.command_set_page_size.definition import (
    set_page_size_definition,
)


class SetPageSizeCommand:
    @staticmethod
    def create(page_size: int) -> str:
        return print_command(set_page_size_definition(), args=[str(page_size)])
