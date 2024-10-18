import os

from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.validate.ArgsValidator import ArgsValidator
from functions.execute.result.ExecutionResult import ExecutionResult
from functions.execute.validate.validate_args import KwargDefinition


def rename_file_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=rename_file,
        verbs=["rename-file", "rf"],
        args_validator=ArgsValidator.file_and_no_args().kwargs(
            required_kwargs=[KwargDefinition.single(["new-name", "new", "to"])]
        ),
        description="Rename a file. Extension will be added by default.",
        category=FunctionCategoryEnum.IngestingFiles,
    )


def rename_file(args_dict: ArgsDict) -> ExecutionResult:
    new_name = args_dict.get_kwarg("new-name")[0] + ".mp3"
    file = args_dict.get_file()
    try:
        os.rename(file.path, file.path[-len(file.filename) :] + new_name)
        file.filename = new_name
        return ExecutionResult.message("ok")  # todo rework these ok messages
    except:
        return ExecutionResult.error_message(
            "Could not rename the file. Check for illegal characters or file permissions."
        )
