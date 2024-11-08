from functions.commands.print_command import print_command

from functions.log.command_show_log.verbs import show_log_verbs


class ShowLogCommand:
    @staticmethod
    def create() -> str:
        return print_command(show_log_verbs)
