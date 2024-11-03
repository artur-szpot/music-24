from functions.commands.print_command import print_command
from functions.file_import.analyze.command_import_files.verbs import import_files_verbs


class ImportFilesCommand:
    @staticmethod
    def create() -> str:
        return print_command(import_files_verbs)
