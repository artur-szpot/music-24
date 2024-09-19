from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition


def mock_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=None,
        verbs=["?"],
        description="This function has not been described yet.",
        category=FunctionCategoryEnum.Unassigned,
    )
