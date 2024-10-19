from functions.commands.print_command import print_command
from functions.help.help_definition import help_definition


class HelpCommand:
    @staticmethod
    def create() -> str:
        return print_command(help_definition())
