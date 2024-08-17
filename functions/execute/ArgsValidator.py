from enum import Enum
from typing import List, Dict, Optional

from functions.definition.ArgsDict import ArgsDict
from functions.execute.arg_validation_errors import (
    NoArgumentsExpectedError,
    ComplexArgumentValidationError,
)
from functions.execute.validate_args import (
    validate_args,
    ArgumentValidationError,
    AllowedKwarg,
)


class ArgsValidatorSpecial(Enum):
    FILENAME_AND_NO_ARGS = 0


class ArgsValidator:
    _min_args: int
    _max_args: int
    _exact_args: int
    _required_kwargs: Dict[str, AllowedKwarg]
    _allowed_kwargs: Dict[str, AllowedKwarg]
    _allowed_flags: List[str]
    _special: Optional[ArgsValidatorSpecial]

    def __init__(
        self,
        min_args: int = 0,
        max_args: int = 0,
        exact_args: int = 0,
        required_kwargs: Dict[str, AllowedKwarg] = None,
        allowed_kwargs: Dict[str, AllowedKwarg] = None,
        allowed_flags: List[str] = None,
        special: ArgsValidatorSpecial = None,
    ):
        self._min_args = min_args
        self._max_args = max_args
        self._exact_args = exact_args
        self._required_kwargs = required_kwargs
        self._allowed_kwargs = allowed_kwargs
        self._allowed_flags = allowed_flags
        self._special = special

    def validate(self, args_dict: ArgsDict) -> ArgsDict:
        do_validate_args = True
        if self._special is not None:
            if self._special == ArgsValidatorSpecial.FILENAME_AND_NO_ARGS:
                args_dict.system["filename"] = self.validate_filename(args_dict)
        if do_validate_args:
            validate_args(
                args_dict,
                min_args=self._min_args,
                max_args=self._max_args,
                exact_args=self._exact_args,
                required_kwargs=self._required_kwargs,
                allowed_kwargs=self._allowed_kwargs,
                allowed_flags=self._allowed_flags,
            )
        return args_dict

    @staticmethod
    def args(min: int = 0, max: int = 0, exact: int = 0):
        return ArgsValidator(min_args=min, max_args=max, exact_args=exact)

    @staticmethod
    def no_args():
        return ArgsValidator()

    @staticmethod
    def filename_and_no_args():
        return ArgsValidator(special=ArgsValidatorSpecial.FILENAME_AND_NO_ARGS)

    def kwargs(
        self,
        required_kwargs: Dict[str, AllowedKwarg] = None,
        allowed_kwargs: Dict[str, AllowedKwarg] = None,
    ):
        self._required_kwargs = required_kwargs
        self._allowed_kwargs = allowed_kwargs
        return self

    def flags(self, allowed_flags: Dict):
        self._allowed_flags = [
            item for variants in allowed_flags.values() for item in variants
        ]
        return self

    def validate_filename(self, args_dict: ArgsDict) -> str:
        try:
            validate_args(
                args_dict,
                exact_args=1,
            )
            return args_dict.args[0]
        except ArgumentValidationError:
            pass

        try:
            required_kwargs_temp = {
                "query": AllowedKwarg.single(),
                "pos": AllowedKwarg.single(),
            }
            required_kwargs_temp.update(self._required_kwargs or {})
            validate_args(
                args_dict,
                required_kwargs=required_kwargs_temp,
                allowed_kwargs=self._allowed_kwargs,
            )
            return "abc"  # todo reading from queries
        except ArgumentValidationError:
            pass

        try:
            required_kwargs_temp = {"filename": AllowedKwarg.single()}
            required_kwargs_temp.update(self._required_kwargs or {})
            validate_args(
                args_dict,
                required_kwargs=required_kwargs_temp,
                allowed_kwargs=self._allowed_kwargs,
            )
            return args_dict.get_kwarg("filename")[0]
        except ArgumentValidationError:
            raise ComplexArgumentValidationError()
