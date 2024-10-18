from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.execute.result.ExecutionResult import ExecutionResult
from functions.file_import.read_files_to_import import read_files_to_import
from functions.file_management.file_operations import create_db_files


def import_files_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=import_files,
        verbs=["import-files", "if"],
        description="Import all files from the import directory.",
        category=FunctionCategoryEnum.IngestingFiles,
    )


def import_files(args_dict: ArgsDict) -> ExecutionResult:
    files = read_files_to_import()
    # move files
    # NOW create file_management files
    create_db_files(files)
    return ExecutionResult.message(f"Successfully imported {len(files)} files")
