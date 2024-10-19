from functions.commands.print_command import print_command
from functions.file_management.command_rename_file.definition import (
    rename_file_definition,
)


class RenameFileCommand:
    @staticmethod
    def create(ordinal: int, new_name: str) -> str:
        return print_command(rename_file_definition(), args=[str(ordinal), new_name])
