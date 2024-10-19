from enum import Enum


class SystemKwargs(Enum):
    Query = "query"
    Position = "pos"
    Filename = "filename"
    Message = "message"
    ErrorMessage = "error-message"

    @staticmethod
    def is_system_kwarg(value: str) -> bool:
        try:
            test = SystemKwargs(value)
            return True
        except:
            return False
