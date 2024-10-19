from functions.commands.print_command import print_command

from functions.log.command_show_log.definition import show_log_definition


class ShowLogCommand:
    @staticmethod
    def create() -> str:
        return print_command(show_log_definition())
