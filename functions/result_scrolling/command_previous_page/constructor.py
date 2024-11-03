from functions.commands.print_command import print_command
from functions.result_scrolling.command_previous_page.verbs import previous_page_verbs


class PreviousPageCommand:
    @staticmethod
    def create() -> str:
        return print_command(previous_page_verbs)
