from enum import Enum
from typing import Optional, List, Dict

from functions.data_types.DataType import DataType


class GenreCategory(Enum):
    MusicType = "type"
    MusicGenre = "genre"
    MusicQuality = "quality"


class Genre(DataType):
    category: GenreCategory

    def __init__(
            self,
            index: int,
            name: str,
            aliases: Optional[List[str]] = None,
            misspellings: Optional[List[str]] = None,
            other: Dict[str, str] = None,
    ):
        DataType.__init__(self, index, name, aliases, misspellings, other)
        self.category = GenreCategory(self.other["category"])

    @staticmethod
    def create(
            name: str,
            aliases: Optional[List[str]] = None,
            misspellings: Optional[List[str]] = None,
            other: Dict[str, str] = None,
    ):
        return Genre(-1, name, aliases, misspellings, other)

    @staticmethod
    def check_capitalization(name: str) -> Optional[str]:
        correct_capitalization = " ".join(
            [word[0].upper() + word[1:].lower() for word in name.split(" ")]
        )
        if name != correct_capitalization:
            return correct_capitalization

    @staticmethod
    def check_legal_name(name: str) -> Optional[str]:
        corrected_name = name.replace(",", "")
        if name != corrected_name:
            return corrected_name
