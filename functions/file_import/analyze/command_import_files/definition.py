from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.file_import.analyze.command_import_files.executor import import_files


def import_files_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=import_files,
        verbs=["import-files", "if"],
        description="Import all files from the import directory.",
        category=FunctionCategoryEnum.IngestingFiles,
    )
