from functions.commands.print_command import print_command
from functions.result_scrolling.command_next_page.definition import next_page_definition


class NextPageCommand:
    @staticmethod
    def create() -> str:
        return print_command(next_page_definition())
