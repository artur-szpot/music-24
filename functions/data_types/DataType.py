from typing import Optional, List, Dict, Any

from libs.list_union_util import SimpleList


class DataType:
    index: int
    name: str
    aliases: Optional[List[str]]
    misspellings: Optional[List[str]]
    other: Dict[str, str]

    def __init__(
        self,
        index: int,
        name: str,
        aliases: Optional[List[str]] = None,
        misspellings: Optional[List[str]] = None,
        other: Dict[str, str] = None,
    ):
        self.index = index
        self.name = name
        self.aliases = aliases
        self.misspellings = misspellings
        self.other = other or {}

    @staticmethod
    def create(
        name: str,
        aliases: Optional[List[str]] = None,
        misspellings: Optional[List[str]] = None,
        other: Dict[str, str] = None,
    ):

        return DataType(-1, name, aliases, misspellings, other)

    @staticmethod
    def from_dict(values: Dict[str, Any]):
        index = values.get("index")
        name = values.get("name")
        aliases = values.get("aliases")
        misspellings = values.get("misspellings")
        other = {
            key: value
            for key, value in values.items()
            if key not in ["index", "name", "aliases", "misspellings"]
        }
        return DataType(index, name, aliases, misspellings, other)

    def to_dict(self) -> Dict[str, SimpleList[str]]:
        base = {
            "index": self.index,
            "name": self.name,
            "aliases": self.aliases,
            "misspellings": self.misspellings,
        }
        base.update(self.other)
        return base
