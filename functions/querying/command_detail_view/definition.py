from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.commands.definition.FunctionFollowingCommands import (
    FunctionFollowingCommands,
)
from functions.execute.validate.ArgsValidator import ArgsValidator
from functions.querying.command_detail_view.executor import detail_view
from functions.querying.command_detail_view.flags import detail_view_flags


def detail_view_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=detail_view,
        verbs=["detail-view", "d"],
        description="Lists details of the chosen file.",
        category=FunctionCategoryEnum.ViewingFiles,
        args_validator=ArgsValidator.file_and_no_args().flags(detail_view_flags),
        following_commands=FunctionFollowingCommands().empty("next-page"),
    )
