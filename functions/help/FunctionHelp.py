from typing import Dict, List

from enums.function_categories import FunctionCategoryEnum


class ParameterHelp:
    description: str
    types: str

    def __init__(self, description: str, types: str):
        self.description = description
        self.types = types


class FunctionHelp:
    description: str
    category: FunctionCategoryEnum
    parameters: Dict[str, ParameterHelp]
    verbs: List[str]

    def __init__(
        self,
        verbs: List[str],
        description: str,
        category: FunctionCategoryEnum,
        parameters: Dict[str, ParameterHelp] = None,
    ):
        self.verbs = verbs
        self.description = description
        self.category = category
        self.parameters = parameters
