from typing import Optional, List

from functions.commands.print_command import print_command
from functions.querying.command_detail_view.definition import detail_view_definition
from functions.querying.command_detail_view.flags import DetailViewFlags


class DetailViewCommand:
    @staticmethod
    def create(flags: Optional[List[DetailViewFlags]]) -> str:
        return print_command(detail_view_definition(), flags=flags)
