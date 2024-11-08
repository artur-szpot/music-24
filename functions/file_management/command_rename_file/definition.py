from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.validate.ArgsValidator import ArgsValidator
from functions.execute.validate.validate_args import KwargDefinition
from functions.file_management.command_rename_file.executor import rename_file
from functions.file_management.command_rename_file.kwargs import (
    RenameFileKwargs,
    rename_file_kwargs,
)
from functions.file_management.command_rename_file.verbs import rename_file_verbs


def rename_file_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=rename_file,
        verbs=rename_file_verbs,
        args_validator=ArgsValidator.file_and_no_args().kwargs(
            required_kwargs=[
                KwargDefinition.single(rename_file_kwargs(RenameFileKwargs.NewName))
            ]
        ),
        description="Rename a file. Extension will be added by default.",
        category=FunctionCategoryEnum.IngestingFiles,
    )
