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


class ArgsExtractor:
    @staticmethod
    def no_args(args_dict: ArgsDict) -> None:
        if args_dict.args or args_dict.kwargs or args_dict.flags:
            raise NoArgumentsExpectedError()

    @staticmethod
    def single_arg(
        args_dict: ArgsDict, required_kwargs=None, allowed_kwargs=None
    ) -> str:
        validate_args(
            args_dict,
            exact_args=1,
            required_kwargs=required_kwargs,
            allowed_kwargs=allowed_kwargs,
        )
        return args_dict.args[0]

    @staticmethod
    def filename(args_dict: ArgsDict, required_kwargs=None, allowed_kwargs=None) -> str:
        try:
            validate_args(
                args_dict,
                exact_args=1,
                required_kwargs=required_kwargs,
                allowed_kwargs=allowed_kwargs,
            )
            return args_dict.args[0]
        except ArgumentValidationError:
            pass

        try:
            required_kwargs_temp = {
                "query": AllowedKwarg.single(),
                "pos": AllowedKwarg.single(),
            }
            required_kwargs_temp.update(required_kwargs or {})
            validate_args(
                args_dict,
                required_kwargs=required_kwargs_temp,
                allowed_kwargs=allowed_kwargs,
            )
            return "abc"  # todo reading from queries
        except ArgumentValidationError:
            pass

        try:
            required_kwargs_temp = {"filename": AllowedKwarg.single()}
            required_kwargs_temp.update(required_kwargs or {})
            validate_args(
                args_dict,
                required_kwargs=required_kwargs_temp,
                allowed_kwargs=allowed_kwargs,
            )
            return args_dict.get_kwarg("filename")[0]
        except ArgumentValidationError:
            raise ComplexArgumentValidationError()
