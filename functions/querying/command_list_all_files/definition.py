from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.commands.definition.FunctionFollowingCommands import (
    FunctionFollowingCommands,
)
from functions.querying.command_list_all_files.executor import list_all_files
from functions.querying.command_list_all_files.verbs import list_all_files_verbs


def list_all_files_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=list_all_files,
        verbs=list_all_files_verbs,
        description="Lists all files currently in the database.",
        category=FunctionCategoryEnum.ViewingFiles,
        following_commands=FunctionFollowingCommands().empty("next-page"),
    )
