from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.help.command_help.executor import print_help


def help_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=print_help,
        verbs=["help", "h"],
        description="Lists all commands with their descriptions.",
        category=FunctionCategoryEnum.AppManagement,
    )
