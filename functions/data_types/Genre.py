from enum import Enum
from typing import Optional, List, Dict, Any

from functions.data_types.DataType import DataType


class GenreCategory(Enum):
    MusicType = 0
    MusicGenre = 1
    MusicQuality = 2


class Genre(DataType):
    category: GenreCategory

    def __init__(
        self,
        name: str,
        index: int,
        category: GenreCategory,
        aliases: Optional[List[str]] = None,
        misspellings: Optional[List[str]] = None,
    ):
        DataType.__init__(self, name, index, aliases, misspellings)
        self.category = category

    @staticmethod
    def from_dict(values: Dict[str, Any]):
        return Genre(
            name=values.get("name"),
            index=values.get("index"),
            category=GenreCategory(values.get("category")),
            aliases=values.get("aliases"),
            misspellings=values.get("misspellings"),
        )

    def to_dict(self) -> Dict[str, Any]:
        super_dict = super().to_dict()
        super_dict.update(
            {
                "category": self.category.value,
            }
        )
        return super_dict
