from enum import Enum


class DetailViewFlags(Enum):
    ErrorsAndWarningsOnly = 0


detail_view_flags = {DetailViewFlags.ErrorsAndWarningsOnly: ["e", "w"]}
