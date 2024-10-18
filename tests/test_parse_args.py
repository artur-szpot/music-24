import unittest

from functions.execute.parse.args_parsing_errors import ArgsParsingError
from functions.execute.parse.parse_args import parse_args
from libs.error_handling import error_message_to_string


class Test(unittest.TestCase):

    # NO ARGS

    def test_should_parse_no_args(self):
        user_input = "command"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(parsed_args.kwargs, {})
        self.assertListEqual(parsed_args.flags, [])

    # JUST ARGS

    def test_should_parse_single_arg(self):
        user_input = "command arg"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, ["arg"])
        self.assertDictEqual(parsed_args.kwargs, {})
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_single_quoted_arg(self):
        user_input = 'command "arg"'
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, ["arg"])
        self.assertDictEqual(parsed_args.kwargs, {})
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_single_arg_with_quotes(self):
        user_input = 'command \\"arg\\"'
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, ['"arg"'])
        self.assertDictEqual(parsed_args.kwargs, {})
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_single_quoted_arg_with_quotes(self):
        user_input = 'command "\\"arg\\""'
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, ['"arg"'])
        self.assertDictEqual(parsed_args.kwargs, {})
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_multiple_args(self):
        user_input = "command arg1 arg2 arg3"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, ["arg1", "arg2", "arg3"])
        self.assertDictEqual(parsed_args.kwargs, {})
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_complex_args(self):
        user_input = 'command arg1 "arg2 arg3" arg4'
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, ["arg1", "arg2 arg3", "arg4"])
        self.assertDictEqual(parsed_args.kwargs, {})
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_complex_args_with_quotes(self):
        user_input = 'command arg1 "arg2 \\"arg3\\"" arg4'
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, ["arg1", 'arg2 "arg3"', "arg4"])
        self.assertDictEqual(parsed_args.kwargs, {})
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_complex_args_with_complex_quotes(self):
        user_input = 'command arg1 "arg2 \\"arg3 arg4\\"" arg5'
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, ["arg1", 'arg2 "arg3 arg4"', "arg5"])
        self.assertDictEqual(parsed_args.kwargs, {})
        self.assertListEqual(parsed_args.flags, [])

    # JUST FLAGS

    def test_should_parse_single_short_flag(self):
        user_input = "command -f"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(parsed_args.kwargs, {})
        self.assertListEqual(parsed_args.flags, ["f"])

    def test_should_parse_multiple_short_flags(self):
        user_input = "command -f -g -h"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(parsed_args.kwargs, {})
        self.assertListEqual(parsed_args.flags, ["f", "g", "h"])

    def test_should_parse_single_long_flag(self):
        user_input = "command --flag"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(parsed_args.kwargs, {})
        self.assertListEqual(parsed_args.flags, ["flag"])

    def test_should_parse_multiple_long_flags(self):
        user_input = "command --flag1 --flag2 --flag3"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(parsed_args.kwargs, {})
        self.assertListEqual(parsed_args.flags, ["flag1", "flag2", "flag3"])

    def test_should_parse_multiple_mixed_flags(self):
        user_input = "command -f --flag2 --flag3 -g"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(parsed_args.kwargs, {})
        self.assertListEqual(parsed_args.flags, ["f", "flag2", "flag3", "g"])

    # JUST KWARGS

    def test_should_parse_single_short_kwarg(self):
        user_input = "command -k 1"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(parsed_args.kwargs, {"k": ["1"]})
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_single_short_kwarg_with_multiple_values(self):
        user_input = "command -k 1 2 3"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(parsed_args.kwargs, {"k": ["1", "2", "3"]})
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_multiple_short_kwargs(self):
        user_input = "command -k 1 -l 2 -m 3"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(parsed_args.kwargs, {"k": ["1"], "l": ["2"], "m": ["3"]})
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_multiple_short_kwargs_with_multiple_values(self):
        user_input = "command -k 1 abc xyz -l 2 666 42 -m 3 4 5"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(
            parsed_args.kwargs,
            {"k": ["1", "abc", "xyz"], "l": ["2", "666", "42"], "m": ["3", "4", "5"]},
        )
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_single_long_kwarg(self):
        user_input = "command --kwarg 1"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(parsed_args.kwargs, {"kwarg": ["1"]})
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_single_long_kwarg_with_multiple_values(self):
        user_input = "command --kwarg 1 2 3"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(parsed_args.kwargs, {"kwarg": ["1", "2", "3"]})
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_multiple_long_kwargs(self):
        user_input = "command --kwarg1 1 --kwarg2 2 --kwarg3 3"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(
            parsed_args.kwargs, {"kwarg1": ["1"], "kwarg2": ["2"], "kwarg3": ["3"]}
        )
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_multiple_long_kwargs_with_multiple_values(self):
        user_input = "command --kwarg1 1 abc xyz --kwarg2 2 666 42 --kwarg3 3 4 5"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(
            parsed_args.kwargs,
            {
                "kwarg1": ["1", "abc", "xyz"],
                "kwarg2": ["2", "666", "42"],
                "kwarg3": ["3", "4", "5"],
            },
        )
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_mixed_kwargs(self):
        user_input = "command --kwarg 1 -k 2"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(parsed_args.kwargs, {"kwarg": ["1"], "k": ["2"]})
        self.assertListEqual(parsed_args.flags, [])

    def test_should_parse_mixed_kwargs_with_multiple_values(self):
        user_input = "command --kwarg1 1 abc xyz -k 2 666 42 --kwarg3 3 4 5"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(
            parsed_args.kwargs,
            {
                "kwarg1": ["1", "abc", "xyz"],
                "k": ["2", "666", "42"],
                "kwarg3": ["3", "4", "5"],
            },
        )
        self.assertListEqual(parsed_args.flags, [])

    # MIXED INPUTS: ARGS AND FLAGS

    def test_should_parse_args_and_flags(self):
        user_input = "command arg1 arg2 -f --flag2"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, ["arg1", "arg2"])
        self.assertDictEqual(parsed_args.kwargs, {})
        self.assertListEqual(parsed_args.flags, ["f", "flag2"])

    # MIXED INPUTS: ARGS AND KWARGS

    def test_should_parse_args_and_kwargs(self):
        user_input = "command arg1 arg2 -k 1 --kwarg2 2"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, ["arg1", "arg2"])
        self.assertDictEqual(parsed_args.kwargs, {"k": ["1"], "kwarg2": ["2"]})
        self.assertListEqual(parsed_args.flags, [])

    # MIXED INPUTS: FLAGS AND KWARGS

    def test_should_parse_flags_and_kwargs(self):
        user_input = "command -f --flag2 -k 1 --kwarg2 2"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, [])
        self.assertDictEqual(parsed_args.kwargs, {"k": ["1"], "kwarg2": ["2"]})
        self.assertListEqual(parsed_args.flags, ["f", "flag2"])

    # MIXED INPUTS: ARGS, FLAGS AND KWARGS

    def test_should_parse_args_flags_and_kwargs(self):
        user_input = "command arg1 arg2 -f --flag2 -k 1 --kwarg2 2"
        parsed_args = parse_args(user_input)
        self.assertListEqual(parsed_args.args, ["arg1", "arg2"])
        self.assertDictEqual(parsed_args.kwargs, {"k": ["1"], "kwarg2": ["2"]})
        self.assertListEqual(parsed_args.flags, ["f", "flag2"])

    # ERRORS: JUST ARGS

    def test_should_error_on_empty_argument(self):
        user_input = 'command arg1 ""'
        try:
            parse_args(user_input)
        except ArgsParsingError as error:
            self.assertEqual(
                error_message_to_string(error),
                'Parsing error: empty arguments ("") are not allowed',
            )
            return
        self.assertEqual("An error should have been thrown", "")

    def test_should_error_on_nested_quoted_argument(self):
        user_input = 'command "arg1 "arg2" arg3"'
        try:
            parse_args(user_input)
        except ArgsParsingError as error:
            self.assertEqual(
                error_message_to_string(error), "Parsing error: nested quoted argument"
            )
            return
        self.assertEqual("An error should have been thrown", "")

    def test_should_error_on_opening_next_quote(self):
        user_input = 'command "arg1 "arg2 arg3"'
        try:
            parse_args(user_input)
        except ArgsParsingError as error:
            self.assertEqual(
                error_message_to_string(error),
                "Parsing error: new quote opened before closing the last",
            )
            return
        self.assertEqual("An error should have been thrown", "")

    def test_should_error_on_closing_too_many_quotes(self):
        user_input = 'command arg1 arg2"'
        try:
            parse_args(user_input)
        except ArgsParsingError as error:
            self.assertEqual(
                error_message_to_string(error),
                "Parsing error: unpaired closing quote",
            )
            return
        self.assertEqual("An error should have been thrown", "")

    def test_should_error_on_misused_quotes_doubled(self):
        user_input = 'command "arg1 arg2""'
        try:
            parse_args(user_input)
        except ArgsParsingError as error:
            self.assertEqual(
                error_message_to_string(error),
                "Parsing error: incorrect quote usage",
            )
            return
        self.assertEqual("An error should have been thrown", "")

    def test_should_error_on_misused_quotes_inset(self):
        user_input = 'command ar"g1 arg2'
        try:
            parse_args(user_input)
        except ArgsParsingError as error:
            self.assertEqual(
                error_message_to_string(error),
                "Parsing error: incorrect quote usage",
            )
            return
        self.assertEqual("An error should have been thrown", "")

    # ERRORS: FLAGS AND KWARGS

    def test_should_error_on_long_flag_with_single_dash(self):
        user_input = "command -flag"
        try:
            parse_args(user_input)
        except ArgsParsingError as error:
            self.assertEqual(
                error_message_to_string(error),
                'Incorrect flag usage: "-flag" should have been "--flag"',
            )
            return
        self.assertEqual("An error should have been thrown", "")

    def test_should_error_on_short_flag_with_two_dashes(self):
        user_input = "command --f"
        try:
            parse_args(user_input)
        except ArgsParsingError as error:
            self.assertEqual(
                error_message_to_string(error),
                'Incorrect flag usage: "--f" should have been "-f"',
            )
            return
        self.assertEqual("An error should have been thrown", "")

    def test_should_error_on_empty_flag_with_single_dash(self):
        user_input = "command -"
        try:
            parse_args(user_input)
        except ArgsParsingError as error:
            self.assertEqual(
                error_message_to_string(error),
                'Incorrect flag usage: "-" lacks flag name',
            )
            return
        self.assertEqual("An error should have been thrown", "")

    def test_should_error_on_empty_flag_with_two_dashes(self):
        user_input = "command --"
        try:
            parse_args(user_input)
        except ArgsParsingError as error:
            self.assertEqual(
                error_message_to_string(error),
                'Incorrect flag usage: "--" lacks flag name',
            )
            return
        self.assertEqual("An error should have been thrown", "")


if __name__ == "__main__":
    unittest.main()
