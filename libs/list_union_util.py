from typing import TypeVar, Union, List, Optional

T = TypeVar('T')

SimpleList = Union[T, List[T]]


def simple_list(value: Optional[SimpleList]) -> List[T]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]
