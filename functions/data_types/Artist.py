from typing import Optional, List, Dict

from functions.data_types.DataType import DataType


class Artist(DataType):

    @staticmethod
    def create(
            name: str,
            aliases: Optional[List[str]] = None,
            misspellings: Optional[List[str]] = None,
            other: Dict[str, str] = None,
    ):
        return Artist(-1, name, aliases, misspellings, other)

    @staticmethod
    def check_legal_name(name: str) -> Optional[str]:
        corrected_name = name.replace(",", "").replace("[,]", "").replace("]", "")
        if name != corrected_name:
            return corrected_name
