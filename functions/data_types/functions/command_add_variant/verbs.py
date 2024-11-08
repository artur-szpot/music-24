from typing import List

from functions.data_types.DataTypeEnum import DataTypeEnum


def add_variant_verbs(data_type: DataTypeEnum, variant_name: str) -> List[str]:
    return [
        f"add-{data_type.value}-{variant_name}",
        f"add-{variant_name}-{data_type.value}",
        f"{data_type.value}-{variant_name}",
        f"{variant_name}-{data_type.value}",
    ]
