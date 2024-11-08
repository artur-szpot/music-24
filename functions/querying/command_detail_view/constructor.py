from typing import Optional, List

from functions.commands.print_command import print_command
from functions.querying.command_detail_view.flags import DetailViewFlags
from functions.querying.command_detail_view.verbs import detail_view_verbs


class DetailViewCommand:
    @staticmethod
    def create(flags: Optional[List[DetailViewFlags]]) -> str:
        return print_command(detail_view_verbs, flags=flags)
