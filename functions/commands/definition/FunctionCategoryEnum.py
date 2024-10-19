from enum import Enum


class FunctionCategoryEnum(Enum):
    AppSettings = "App settings"
    DataTypeManagement = "Data type management"
    AppManagement = "App management"
    ViewingFiles = "View files"
    EditingFiles = "Edit files"
    IngestingFiles = "Ingest new files"
    CreatingPlaylists = "Create playlists"
    ExportingFiles = "Export files"
    Unassigned = "WIP, not yet described"
