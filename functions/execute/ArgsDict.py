from typing import List, Dict


class ArgsDict:
    def __init__(self, args: List[str], kwargs: Dict[str, List[str]], flags: List[str]):
        self.args = args
        self.kwargs = kwargs
        self.flags = flags

    def get_kwarg(self, name: str) -> List[str]:
        return self.kwargs.get(name, [])
