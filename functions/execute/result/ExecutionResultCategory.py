from enum import Enum


class ExecutionResultCategory(Enum):
    Action = -1
    Query = 0
    Detail = 1
    Message = 2
