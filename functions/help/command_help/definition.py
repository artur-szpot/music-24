from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.help.command_help.executor import print_help
from functions.help.command_help.verbs import help_verbs


def help_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=print_help,
        verbs=help_verbs,
        description="Lists all commands with their descriptions.",
        category=FunctionCategoryEnum.AppManagement,
    )
