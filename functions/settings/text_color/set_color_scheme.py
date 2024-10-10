from functions.commands.definition.ActionEnum import ActionEnum
from functions.commands.definition.ArgsDict import ArgsDict
from functions.commands.definition.FunctionCategoryEnum import FunctionCategoryEnum
from functions.commands.definition.FunctionDefinition import FunctionDefinition
from functions.execute.ArgsValidator import ArgsValidator
from functions.execute.ExecutionResult import ExecutionResult, ExecutionResultCategory
from functions.lines.Line import Line

from functions.settings.text_color.ColorScheme import ColorScheme
from functions.settings.app_settings import app_settings
from libs.strings import quoted


def set_color_scheme_definition() -> FunctionDefinition:
    return FunctionDefinition(
        function=set_color_scheme,
        verbs=["color-scheme", "cs"],
        args_validator=ArgsValidator.args(max=1),
        description="Check or set the color scheme of the application",
        category=FunctionCategoryEnum.AppSettings,
    )


def set_color_scheme(args_dict: ArgsDict) -> ExecutionResult:
    color_scheme = args_dict.get_arg()
    if color_scheme is None:
        return ExecutionResult(
            message=Line.simple(
                f"Color scheme is set to {quoted(app_settings.color_scheme.value)}."
            ),
            action=ActionEnum.Refresh,
            category=ExecutionResultCategory.Message,
        )
    try:
        new_scheme = ColorScheme(color_scheme.lower())
    except ValueError:
        return ExecutionResult(
            message=Line.simple(f"Unknown color scheme: {quoted(color_scheme)}."),
            action=ActionEnum.Refresh,
            category=ExecutionResultCategory.Message,
        )
    if app_settings.color_scheme == new_scheme:
        return ExecutionResult(
            message=Line.simple(
                f"Color scheme was already set to {quoted(color_scheme)}."
            ),
            action=ActionEnum.Refresh,
            category=ExecutionResultCategory.Message,
        )
    app_settings.set("color_scheme", new_scheme.value)
    return ExecutionResult.action(ActionEnum.Refresh)
