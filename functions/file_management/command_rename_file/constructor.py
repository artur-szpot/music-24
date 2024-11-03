from functions.commands.print_command import print_command
from functions.file_management.command_rename_file.kwargs import (
    RenameFileKwargs,
    rename_file_kwargs,
)
from functions.file_management.command_rename_file.verbs import rename_file_verbs


class RenameFileCommand:
    @staticmethod
    def create(ordinal: int, new_name: str) -> str:
        return print_command(
            rename_file_verbs,
            args=[str(ordinal)],
            kwargs=[{RenameFileKwargs.NewName: new_name}],
            kwarg_dict=rename_file_kwargs,
        )
