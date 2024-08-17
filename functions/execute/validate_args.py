from typing import List, Dict

from functions.definition.ArgsDict import ArgsDict
from functions.execute.arg_validation_errors import (
    ArgumentValidationError,
    NoArgumentsExpectedError,
)


class AllowedKwarg:
    min_values: int
    max_values: int
    exact_values: int

    def __init__(self, min_values: int = 0, max_values: int = 0, exact_values: int = 0):
        self.min_values = min_values
        self.max_values = max_values
        self.exact_values = exact_values

    @staticmethod
    def single():
        return AllowedKwarg(exact_values=1)

    @staticmethod
    def any():
        return AllowedKwarg(min_values=1)


def validate_kwarg(values: List[str], name: str, props: AllowedKwarg) -> None:
    min_values = props.min_values
    max_values = props.max_values
    exact_values = props.exact_values
    if len(values) < min_values:
        raise ArgumentValidationError(
            f'Not enough values provided for argument "{name}" - expected at least {min_values}, got {len(values)}'
        )
    if len(values) > max_values:
        raise ArgumentValidationError(
            f'Too many values provided for argument "{name}" - expected at most {max_values}, got {len(values)}'
        )
    if exact_values and len(values) != exact_values:
        raise ArgumentValidationError(
            f'Wrong number of values provided for argument "{name}" - expected {exact_values}, got {len(values)}'
        )


def validate_args(
    args_dict: ArgsDict,
    min_args: int = 0,
    max_args: int = 0,
    exact_args: int = 0,
    required_kwargs: Dict[str, AllowedKwarg] = None,
    allowed_kwargs: Dict[str, AllowedKwarg] = None,
    allowed_flags: List[str] = None,
):
    required_kwargs = required_kwargs or {}
    allowed_kwargs = allowed_kwargs or {}
    allowed_flags = allowed_flags or []

    args = args_dict.args
    if len(args) < min_args:
        raise ArgumentValidationError(
            f"Not enough arguments provided - expected at least {min_args}, got {len(args)}"
        )
    if max_args and len(args) > max_args:
        raise ArgumentValidationError(
            f"Too many arguments provided - expected at most {max_args}, got {len(args)}"
        )
    if exact_args and len(args) != exact_args:
        raise ArgumentValidationError(
            f"Wrong number of arguments provided - expected {exact_args}, got {len(args)}."
        )
    if not min_args and not max_args and not exact_args and len(args):
        raise NoArgumentsExpectedError()

    kwargs = args_dict.kwargs
    for name, values in required_kwargs.items():
        kwarg = kwargs.get(name)
        if kwarg is None:
            raise ArgumentValidationError(f'Required argument "--{kwarg}" not supplied')
        validate_kwarg(kwarg, name, values)

    for name, values in allowed_kwargs.items():
        kwarg = kwargs.get(name)
        if kwarg is not None:
            validate_kwarg(kwarg, name, values)

    all_allowed_kwargs = [key for key in allowed_kwargs.keys()] + [
        key for key in allowed_kwargs.keys()
    ]
    disallowed_kwargs = [key for key in kwargs.keys() if key not in all_allowed_kwargs]
    disallowed_flags = [flag for flag in args_dict.flags if flag not in allowed_flags]
    disallowed_args = disallowed_kwargs + disallowed_flags

    if len(disallowed_args):
        raise ArgumentValidationError(
            f'Unexpected keyword arguments and/or flags provided: {", ".join(disallowed_args)}'
        )
