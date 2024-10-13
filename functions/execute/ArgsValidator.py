from enum import Enum
from typing import List, Dict, Any

from functions.cache import cache
from functions.commands.definition.ArgsDict import ArgsDict
from functions.execute.arg_validation_errors import (
    ComplexArgumentValidationError,
)
from functions.execute.validate_args import (
    validate_args,
    ArgumentValidationError,
    KwargDefinition,
)
from libs.error_handling import error_message_to_string
from libs.list_union_util import SimpleList, simple_list
from libs.strings import quoted


class ArgsValidatorSpecial(Enum):
    FILE_AND_NO_ARGS = 0
    CURRENT_FILE = 1


SYSTEM_KWARGS = ["query", "pos", "filename"]


class ArgsValidator:
    _min_args: int
    _max_args: int
    _exact_args: int
    _required_kwargs: Dict[str, KwargDefinition]
    _allowed_kwargs: Dict[str, KwargDefinition]
    _allowed_flags: List[str]
    _special: List[ArgsValidatorSpecial]
    _variants: Dict[str, List[str]]

    def __init__(
        self,
        min_args: int = 0,
        max_args: int = 0,
        exact_args: int = 0,
        special: List[ArgsValidatorSpecial] = None,
    ):
        self._min_args = min_args
        self._max_args = max_args
        self._exact_args = exact_args
        self._required_kwargs = {}
        self._allowed_kwargs = {}
        self._allowed_flags = []
        self._special = special or []
        self._variants = {}

    def validate(self, args_dict: ArgsDict) -> ArgsDict:
        do_validate_args = True
        if ArgsValidatorSpecial.FILE_AND_NO_ARGS in self._special:
            args_dict = self.validate_filename(args_dict)
        if do_validate_args:
            validate_args(
                args_dict,
                min_args=self._min_args,
                max_args=self._max_args,
                exact_args=self._exact_args,
                required_kwargs=self._required_kwargs,
                allowed_kwargs=self._allowed_kwargs,
                allowed_flags=self._allowed_flags,
                variants=self._variants,
            )
        return args_dict

    @staticmethod
    def args(min: int = 0, max: int = 0, exact: int = 0):
        return ArgsValidator(min_args=min, max_args=max, exact_args=exact)

    @staticmethod
    def no_args():
        return ArgsValidator()

    @staticmethod
    def file_and_no_args():
        return ArgsValidator(special=[ArgsValidatorSpecial.FILE_AND_NO_ARGS])

    def kwargs(
        self,
        required_kwargs: List[KwargDefinition] = None,
        allowed_kwargs: List[KwargDefinition] = None,
    ):
        if required_kwargs:
            for definition in required_kwargs:
                kwarg_aliases = definition.aliases
                if len(kwarg_aliases) > 1:
                    self._variants[kwarg_aliases[0]] = kwarg_aliases[1:]
                    for index, sub_kwarg in enumerate(kwarg_aliases):
                        self.check_argument(sub_kwarg)
                        if not index:
                            self._required_kwargs.update({sub_kwarg: definition})
                else:
                    self.check_argument(kwarg_aliases[0])
                    self._required_kwargs.update({kwarg_aliases[0]: definition})
        if allowed_kwargs:
            for definition in allowed_kwargs:
                kwarg_aliases = definition.aliases
                if len(kwarg_aliases) > 1:
                    self._variants[kwarg_aliases[0]] = kwarg_aliases[1:]
                    for index, sub_kwarg in enumerate(kwarg_aliases):
                        self.check_argument(sub_kwarg)
                        if not index:
                            self._allowed_kwargs.update({sub_kwarg: definition})
                else:
                    self.check_argument(kwarg_aliases[0])
                    self._allowed_kwargs.update({kwarg_aliases[0]: definition})
        return self

    def flags(self, allowed_flags: Dict[Any, SimpleList[str]]):
        for flags_raw in allowed_flags.values():
            flags = simple_list(flags_raw)
            for flag in flags:
                self.check_argument(flag)
            self._allowed_flags.extend(flags)
            if len(flags) > 1:
                self._variants[flags[0]] = flags[1:]
        return self

    def check_argument(self, value: str) -> None:
        if value in SYSTEM_KWARGS:
            raise KeyError(
                f"{quoted(value)} is reserved and cannot be used as an argument."
            )
        if (
            value in self._allowed_kwargs
            or value in self._required_kwargs
            or value in self._allowed_flags
        ):
            raise KeyError(f"Argument {quoted(value)} used more than once.")

    def validate_filename(self, args_dict: ArgsDict) -> ArgsDict:
        query_index = None
        try:
            validate_args(
                args_dict,
                exact_args=1,
                required_kwargs=self._required_kwargs,
                allowed_kwargs=self._allowed_kwargs,
                allowed_flags=self._allowed_flags,
                variants=self._variants,
            )
            arg = args_dict.args[0]
            args_dict.args = []
            if arg.isnumeric():
                query_index = int(arg)
            else:
                args_dict.system["filename"] = arg
                return args_dict
        except ArgumentValidationError:
            pass

        try:
            required_kwargs_temp = {"filename": KwargDefinition.single("")}
            required_kwargs_temp.update(self._required_kwargs or {})
            validate_args(
                args_dict,
                min_args=self._min_args,
                max_args=self._max_args,
                exact_args=self._exact_args,
                required_kwargs=required_kwargs_temp,
                allowed_kwargs=self._allowed_kwargs,
                allowed_flags=self._allowed_flags,
                variants=self._variants,
            )
            args_dict.kwargs.pop("filename", None)
            args_dict.system["filename"] = args_dict.get_kwarg("filename")[0]
            return args_dict
        except ArgumentValidationError:
            pass

        try:
            allowed_kwargs_temp = {
                "query": KwargDefinition.single(""),
                "pos": KwargDefinition.single(""),
            }
            allowed_kwargs_temp.update(self._allowed_kwargs or {})
            validate_args(
                args_dict,
                min_args=self._min_args,
                max_args=self._max_args,
                exact_args=self._exact_args,
                required_kwargs=self._required_kwargs,
                allowed_kwargs=allowed_kwargs_temp,
                allowed_flags=self._allowed_flags,
                variants=self._variants,
            )
            args_dict.kwargs.pop("query", None)
            args_dict.kwargs.pop("pos", None)
            if args_dict.kwargs.get("query") is not None:
                args_dict.system["filename"] = "abc"  # todo reading from queries
                return args_dict
            else:
                last_result = cache.get_last_query()
                if last_result:
                    index = args_dict.kwargs.get("pos", query_index)
                    if index < 1 or index > last_result.get_total_items():
                        raise KeyError(
                            f"Index outside of range. Use a value between 1 and {last_result.get_total_items()}."
                        )
                    if index is not None:
                        cache.set_current_file(last_result.get_file(index - 1))
                    else:
                        raise ArgumentValidationError()
                else:
                    raise ArgumentValidationError()
                return args_dict
        except ArgumentValidationError:
            raise ComplexArgumentValidationError()
        except KeyError as error:
            raise ArgumentValidationError(error_message_to_string(error))
