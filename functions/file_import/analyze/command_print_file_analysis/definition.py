from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.commands.definition.FunctionFollowingCommands import (
    FunctionFollowingCommands,
)
from functions.execute.validate.ArgsValidator import ArgsValidator
from functions.file_import.analyze.command_print_file_analysis.executor import (
    print_file_analysis,
)
from functions.file_import.analyze.command_print_file_analysis.flags import (
    print_file_analysis_flags,
)


def print_file_analysis_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=print_file_analysis,
        verbs=["analyze-import", "ai"],
        args_validator=ArgsValidator.no_args().flags(print_file_analysis_flags),
        description="Analyze files from the import directory before importing.",
        category=FunctionCategoryEnum.IngestingFiles,
        following_commands=FunctionFollowingCommands().empty("next-page"),
    )
