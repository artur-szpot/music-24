from functions.commands.print_command import print_command
from functions.result_scrolling.command_set_page_number.definition import (
    set_page_number_definition,
)


class SetPageNumberCommand:
    @staticmethod
    def create(page_number: int) -> str:
        return print_command(set_page_number_definition(), args=[str(page_number)])
