from typing import List, Dict

from functions.commands.definition.ArgsDict import ArgsDict
from functions.execute.args.KwargDefinition import KwargDefinition
from functions.execute.args.system_kwargs import SystemKwargs
from functions.execute.validate.arg_validation_errors import (
    ArgumentValidationError,
    NoArgumentsExpectedError,
)
from functions.execute.validate.validate_kwarg import validate_kwarg


def validate_args(
    args_dict: ArgsDict,
    min_args: int = 0,
    max_args: int = 0,
    exact_args: int = 0,
    required_kwargs: Dict[str, KwargDefinition] = None,
    allowed_kwargs: Dict[str, KwargDefinition] = None,
    allowed_flags: List[str] = None,
    variants: Dict[str, List[str]] = None,
):
    required_kwargs = required_kwargs or {}
    allowed_kwargs = allowed_kwargs or {}
    allowed_flags = allowed_flags or []

    args = args_dict.args
    kwargs = args_dict.kwargs
    flags = args_dict.flags

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

    all_allowed_kwargs = []

    for name, values in required_kwargs.items():
        kwarg_variants = [name] + variants.get(name, [])
        all_allowed_kwargs.extend(kwarg_variants)
        kwarg = None
        for variant in kwarg_variants:
            if kwarg is None:
                kwarg = kwargs.get(variant)
        if kwarg is None:
            raise ArgumentValidationError(f'Required argument "--{name}" not supplied')
        validate_kwarg(kwarg, name, values)

    for name, values in allowed_kwargs.items():
        kwarg_variants = [name] + variants.get(name, [])
        all_allowed_kwargs.extend(kwarg_variants)
        kwarg = None
        for variant in kwarg_variants:
            if kwarg is None:
                kwarg = kwargs.get(variant)
        if kwarg is not None:
            validate_kwarg(kwarg, name, values)

    disallowed_kwargs = [
        key
        for key in kwargs.keys()
        if key not in all_allowed_kwargs and not SystemKwargs.is_system_kwarg(key)
    ]
    disallowed_flags = [flag for flag in flags if flag not in allowed_flags]
    disallowed_args = disallowed_kwargs + disallowed_flags

    if len(disallowed_args):
        raise ArgumentValidationError(
            f'Unexpected keyword arguments and/or flags provided: {", ".join(disallowed_args)}'
        )

    repeated_kwargs_and_flags: List[str] = []
    for main, other in variants.items():
        occurrences = []
        for key in [main] + other:
            if key in kwargs.keys():
                occurrences.append(main)
        for key in [main] + other:
            if key in flags:
                occurrences.append(main)
        if len(occurrences) > 1:
            repeated_kwargs_and_flags.append(occurrences[0])

    if len(repeated_kwargs_and_flags):
        raise ArgumentValidationError(
            f'Repeated use of the following arguments and/or flags: {", ".join(repeated_kwargs_and_flags)}'
        )
