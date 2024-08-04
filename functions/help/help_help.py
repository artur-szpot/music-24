from enums.function_categories import FunctionCategoryEnum
from functions.help.FunctionHelp import FunctionHelp


def mock_help() -> FunctionHelp:
    return FunctionHelp(
        ["?"],
        "This function has not been described yet.",
        FunctionCategoryEnum.Unassigned,
    )


def help_help() -> FunctionHelp:
    return FunctionHelp(
        ["help", "h"],
        "Lists all commands with their descriptions.",
        FunctionCategoryEnum.AppManagement,
    )
