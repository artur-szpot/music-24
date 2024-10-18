from typing import List

from libs.list_union_util import SimpleList, simple_list


class KwargDefinition:
    aliases: List[str]
    min_values: int
    max_values: int
    exact_values: int

    def __init__(
        self,
        aliases: SimpleList[str],
        min_values: int = 0,
        max_values: int = 0,
        exact_values: int = 0,
    ):
        self.aliases = simple_list(aliases)
        self.min_values = min_values
        self.max_values = max_values
        self.exact_values = exact_values

    @staticmethod
    def single(aliases: SimpleList[str]):
        return KwargDefinition(aliases, exact_values=1)

    @staticmethod
    def any(aliases: SimpleList[str]):
        return KwargDefinition(aliases, min_values=1)
