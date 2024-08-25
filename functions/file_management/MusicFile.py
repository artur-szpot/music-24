from enum import Enum
from typing import List, Dict, Any, Optional


class MusicFileDbProps(Enum):
    Desynced = 0


class MusicFileViewProps(Enum):
    OrdinalNumber = 0
    Highlighted = 1


class MusicFile:
    authors: List[str]
    genres: List[str]
    title: Optional[str]
    path: str
    filename: Optional[ str]
    length: Optional[int]
    rating: Optional[int]
    is_mlp: Optional[bool]
    is_dad: Optional[bool]
    is_ready: Optional[bool]
    errors: List[str]
    warnings: List[str]
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

    def get_db_prop(self, prop: int) -> Any:
        return self.db_props.get(prop)

    def set_view_props(self, ordinal_number: int, highlighted: bool = False) -> None:
        self.view_props = {
            MusicFileViewProps.OrdinalNumber: ordinal_number,
            MusicFileViewProps.Highlighted: highlighted,
        }

    def get_ordinal_number(self) -> int:
        return self.view_props.get(MusicFileViewProps.OrdinalNumber, 0)

    def get_highlighted(self) -> bool:
        return self.view_props.get(MusicFileViewProps.Highlighted, False)
