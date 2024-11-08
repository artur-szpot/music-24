from functions.commands.print_command import print_command
from functions.settings.text_color.command_set_page_size.verbs import (
    set_page_size_verbs,
)


class SetPageSizeCommand:
    @staticmethod
    def create(page_size: int) -> str:
        return print_command(set_page_size_verbs, args=[str(page_size)])
