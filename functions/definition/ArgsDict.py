from typing import List, Dict, Any


class ArgsDict:
    def __init__(
        self,
        args: List[str],
        kwargs: Dict[str, List[str]],
        flags: List[str],
        system: Dict[str, Any] = None,
    ):
        self.args = args
        self.kwargs = kwargs
        self.flags = flags
        self.system = system

    def get_kwarg(self, name: str) -> List[str]:
        return self.kwargs.get(name, [])
