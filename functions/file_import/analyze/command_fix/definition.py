from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.commands.definition.FunctionFollowingCommands import (
    FunctionFollowingCommands,
)
from functions.execute.validate.ArgsValidator import ArgsValidator
from functions.file_import.analyze.command_fix.executor import fix
from functions.file_import.analyze.command_fix.verbs import fix_verbs


def fix_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=fix,
        verbs=fix_verbs,
        args_validator=ArgsValidator.args(min=0, max=100),
        description="Fix detected problems in the file by applying suggested changes.",
        category=FunctionCategoryEnum.IngestingFiles,
        following_commands=FunctionFollowingCommands()
        .empty("fix 1")
        .default_prefix("fix"),
    )
