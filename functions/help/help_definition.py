from functions.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.definition.FunctionDefinition import FunctionDefinition
from functions.help.help import print_help


def help_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=print_help,
        verbs=["help", "h"],
        description="Lists all commands with their descriptions.",
        category=FunctionCategoryEnum.AppManagement,
    )
