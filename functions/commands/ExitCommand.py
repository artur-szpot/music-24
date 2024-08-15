from functions.definition.ActionEnum import ActionEnum
from functions.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.definition.FunctionDefinition import FunctionDefinition
from functions.commands.action_result_function import action_result_function


def exit_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=action_result_function(ActionEnum.Return),
        verbs=["exit", "x"],
        description="Closes the application.",
        category=FunctionCategoryEnum.AppManagement,
    )
