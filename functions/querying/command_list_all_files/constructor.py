from functions.commands.print_command import print_command
from functions.querying.command_list_all_files.definition import (
    list_all_files_definition,
)
from functions.querying.command_list_all_files.verbs import list_all_files_verbs


class ListAllFilesCommand:
    @staticmethod
    def create() -> str:
        return print_command(list_all_files_verbs)
