from functions.commands.print_command import print_command

from functions.help.command_help.verbs import help_verbs


class HelpCommand:
    @staticmethod
    def create() -> str:
        return print_command(help_verbs)
