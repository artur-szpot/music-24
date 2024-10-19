from typing import List, Optional

from functions.commands.print_command import print_command
from functions.file_import.analyze.command_print_file_analysis.definition import (
    print_file_analysis_definition,
)
from functions.file_import.analyze.command_print_file_analysis.flags import (
    PrintFileAnalysisFlags,
)


class PrintFileAnalysisCommand:
    @staticmethod
    def create(flags: Optional[List[PrintFileAnalysisFlags]]) -> str:
        return print_command(print_file_analysis_definition(), flags=flags)
