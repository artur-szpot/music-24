from typing import List, Optional, Tuple

from functions.cache import cache
from functions.commands.definition.ArgsDict import ArgsDict
from functions.execute.result.ExecutionResult import ExecutionResult
from functions.execute.validate.arg_validation_errors import ArgumentValidationError
from functions.file_import.analyze.analyze_files import analyze_file
from functions.lines.Line import Line
from functions.music_file.MusicFile import MusicFile
from functions.music_file.MusicFileError import MusicFileError
from functions.querying.file_view_header import file_view_header
from functions.settings.text_color.SchemeColor import SchemeColor
from libs.strings import quoted


def fix(args_dict: ArgsDict) -> ExecutionResult:
    file = args_dict.get_file()
    if file is None:
        return ExecutionResult.error_message("Could not find the file to fix.")
    file = analyze_file(file)
    chosen_option = args_dict.get_numeric_arg(0)
    to_fix, is_error = get_first_to_fix(file)
    if to_fix is None:
        if len(file.errors) or len(file.warnings):
            cache.extend_command_stack(
                f"detail-view {file.get_ordinal_number()} "
                f'--error-message "Remaining problems cannot be fixed automatically."'
            )
        else:
            cache.extend_command_stack(
                f'detail-view {file.get_ordinal_number()} --message "Nothing left to fix."'
            )
        return ExecutionResult.refresh()
    if chosen_option is None:
        return ExecutionResult.paginable(
            items=fix_exe(to_fix, is_error), header=[file_view_header(file)]
        )
    if chosen_option < 1 or chosen_option > len(to_fix.fixes):
        raise ArgumentValidationError(
            f"Incorrect option chosen. Provide a number between 1 and {len(to_fix.fixes)}."
        )
    chosen_fix = to_fix.fixes[chosen_option - 1]
    args = (
        " ".join(quoted(arg) for arg in args_dict.args[1:])
        if chosen_fix.with_user_input
        else ""
    )
    cache.extend_command_stack(
        [
            f"{chosen_fix.command} {args}",
            "fix",
        ]
    )
    return ExecutionResult.refresh()


def get_first_to_fix(file: MusicFile) -> Tuple[Optional[MusicFileError], bool]:
    is_error = False
    if not file.errors and not file.warnings:
        return None, is_error
    to_fix = None
    errors = file.errors[:]
    warnings = file.warnings[:]
    while to_fix is None:
        if errors:
            to_fix = errors.pop(0)
            is_error = True
        if to_fix is None and warnings:
            to_fix = warnings.pop(0)
        if to_fix is None:
            break
        if not len(to_fix.fixes):
            to_fix = None
            is_error = False
    return to_fix, is_error


def fix_exe(to_fix: MusicFileError, is_error: bool) -> List[Line]:
    details = []
    if is_error:
        details.append(Line.key_value("Error", to_fix.text, key_color=SchemeColor.BAD))
    else:
        details.append(
            Line.key_value("Warning", to_fix.text, key_color=SchemeColor.WARN)
        )
    details.append(Line.empty())
    details.append(Line.bold("Fix options:"))
    for index, proposition in enumerate(to_fix.fixes):
        details.append(Line.key_value(str(index + 1), proposition.text))
    return details
