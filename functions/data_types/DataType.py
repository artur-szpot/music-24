import json
from enum import Enum
from typing import Optional, List, Dict, Any
from functions.data_types.genre_registry import genre_registry


class DataType:
    name: str
    index: int
    aliases: Optional[List[str]]
    misspellings: Optional[List[str]]

    def __init__(self,
    name: str,
    index: int,
    aliases: Optional[List[str]]=None,
    misspellings: Optional[List[str]]=None):
        self.name = name
        self.index=index
        self.aliases=aliases
        self.misspellings=misspellings

    @staticmethod
    def from_dict(values: Dict[str, Any]):
        return DataType(
            name=values.get("name"),
            index=values.get("index"),
            aliases=values.get("aliases"),
            misspellings=values.get("misspellings"),
        )


    def to_dict(self)->Dict[str, Any]:
        return {
            'name':self.name,
            'index':self.index,
            'aliases':self.aliases,
            'misspellings':self.misspellings,
        }




