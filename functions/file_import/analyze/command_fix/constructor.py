from typing import List

from functions.commands.print_command import print_command

# todo this doesn't make sense while we cannot distinguish ints
# or does it?
from functions.file_import.analyze.command_fix.verbs import fix_verbs


class FixCommand:
    @staticmethod
    def create(chosen_option: int, args: List[str]) -> str:
        return print_command(fix_verbs, args=[str(chosen_option)] + args)
