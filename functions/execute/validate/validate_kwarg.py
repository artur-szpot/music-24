from typing import List

from functions.execute.validate.arg_validation_errors import (
    ArgumentValidationError,
)
from functions.execute.args.KwargDefinition import KwargDefinition
from libs.strings import quoted


def validate_kwarg(values: List[str], name: str, props: KwargDefinition) -> None:
    min_values = props.min_values
    max_values = props.max_values
    exact_values = props.exact_values
    if len(values) < min_values:
        raise ArgumentValidationError(
            f"Not enough values provided for argument {quoted(name)} - expected at least {min_values}, got {len(values)}"
        )
    if max_values and len(values) > max_values:
        raise ArgumentValidationError(
            f"Too many values provided for argument {quoted(name)} - expected at most {max_values}, got {len(values)}"
        )
    if exact_values and len(values) != exact_values:
        raise ArgumentValidationError(
            f"Wrong number of values provided for argument {quoted(name)} - expected {exact_values}, got {len(values)}"
        )
