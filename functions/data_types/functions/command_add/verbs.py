from typing import List

from functions.data_types.DataTypeEnum import DataTypeEnum


def add_verbs(data_type: DataTypeEnum) -> List[str]:
    return [f"add-{data_type.value}"]
