from typing import List

from functions.commands.print_command import print_command
from functions.file_import.analyze.command_fix.definition import fix_definition


# todo this doesn't make sense while we cannot distinguish ints
# or does it?
class FixCommand:
    @staticmethod
    def create(chosen_option: int, args: List[str]) -> str:
        return print_command(fix_definition(), args=[str(chosen_option)] + args)
