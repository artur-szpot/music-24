from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.help.command_mock.executor import mock_function


def mock_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=mock_function,
        verbs=["?"],
        description="This function has not been described yet.",
        category=FunctionCategoryEnum.Unassigned,
    )
