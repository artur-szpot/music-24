from functions.commands.print_command import print_command
from functions.file_management.command_clear_db.verbs import clear_db_verbs


class ClearDbCommand:
    @staticmethod
    def create() -> str:
        return print_command(clear_db_verbs)
