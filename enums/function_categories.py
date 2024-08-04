from enum import Enum


class FunctionCategoryEnum(Enum):
    AppManagement = 0
    ViewingFiles = 1
    EditingFiles = 2
    IngestingFiles = 3
    CreatingPlaylists = 4
    ExportingFiles = 5
    Unassigned = -1
