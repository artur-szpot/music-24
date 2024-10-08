from typing import List, Dict, Any, Optional

from functions.music_file.MusicFileDbProps import MusicFileDbProps
from functions.music_file.MusicFileError import MusicFileError
from functions.music_file.MusicFileViewProps import MusicFileViewProps


class MusicFile:
    authors: List[str]
    genres: List[str]
    title: Optional[str]
    path: str
    filename: Optional[str]
    length: Optional[int]
    rating: Optional[int]
    is_mlp: Optional[bool]
    is_dad: Optional[bool]
    is_ready: Optional[bool]

    predicted_authors: Optional[List[str]]
    predicted_title: Optional[str]

    errors: List[MusicFileError]
    warnings: List[MusicFileError]

    db_props: Dict[MusicFileDbProps, Any]
    view_props: Dict[MusicFileViewProps, Any]

    def __init__(self, source) -> None:
        self.authors = source.get("authors", [])
        self.genres = source.get("genres", [])
        self.title = source.get("title")
        self.path = source.get("path")
        self.filename = source.get("filename")
        self.length = source.get("length")
        self.rating = source.get("rating")
        self.is_mlp = source.get("is_mlp")
        self.is_dad = source.get("is_dad")
        self.is_ready = source.get("is_ready")
        self.errors = source.get("errors", [])
        self.warnings = source.get("warnings", [])
        self.predicted_authors = source.get("predicted_authors", [])
        self.predicted_title = source.get("predicted_title", "")
        self.db_props = source.get("db_props", {})
        self.view_props = source.get("view_props", {})

    def to_dict(self):
        return {
            "authors": self.authors,
            "genres": self.genres,
            "title": self.title,
            "path": self.path,
            "filename": self.filename,
            "length": self.length,
            "rating": self.rating,
            "is_mlp": self.is_mlp,
            "is_dad": self.is_dad,
            "is_ready": self.is_ready,
        }

    def set_db_prop(self, prop, value: Any) -> None:
        self.db_props[prop] = value

    def get_db_prop(self, prop: MusicFileDbProps) -> Any:
        return self.db_props.get(prop)

    def set_view_props(self, ordinal_number: int, highlighted: bool = False) -> None:
        self.view_props = {
            MusicFileViewProps.OrdinalNumber: ordinal_number + 1,
            MusicFileViewProps.Highlighted: highlighted,
        }

    def get_ordinal_number(self) -> int:
        return self.view_props.get(MusicFileViewProps.OrdinalNumber, 0)

    def get_highlighted(self) -> bool:
        return self.view_props.get(MusicFileViewProps.Highlighted, False)
