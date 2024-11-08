from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.validate.ArgsValidator import ArgsValidator

from functions.settings.text_color.command_set_color_scheme.executor import (
    set_color_scheme,
)
from functions.settings.text_color.command_set_color_scheme.verbs import (
    set_color_scheme_verbs,
)


def set_color_scheme_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=set_color_scheme,
        verbs=set_color_scheme_verbs,
        args_validator=ArgsValidator.args(max=1),
        description="Check or set the color scheme of the application",
        category=FunctionCategoryEnum.AppSettings,
    )
