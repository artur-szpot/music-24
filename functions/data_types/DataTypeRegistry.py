import json
from typing import Optional, List, Dict
from typing import TypeVar, Generic

from functions.data_types.DataType import DataType
from libs.io import create_directory

T = TypeVar("T", bound=DataType)


class DataTypeRegistry(Generic[T]):
    data: Dict[int, T]
    _free_index: int

    @staticmethod
    def get_data_type():
        return DataType

    @staticmethod
    def get_data_type_name() -> str:
        return ""

    def __init__(self):
        self._free_index = 0
        try:
            with open(
                f"db/data/{self.get_data_type_name()}.json", mode="r"
            ) as current_file:
                my_type = self.get_data_type()
                self.data = {
                    value["index"]: my_type.from_dict(value)
                    for value in json.loads(current_file.read())
                }
        except Exception as e:
            self.data = {}
        self.get_free_index()

    def get_free_index(self) -> int:
        existing_indices = set(self.data.keys())
        while self._free_index in existing_indices:
            self._free_index += 1
        return self._free_index

    def get(self, index: int) -> Optional[T]:
        return self.data.get(index)

    def find(self, name: str) -> Optional[T]:
        for datum in self.data.values():
            if datum.name == name or name in datum.aliases:
                return datum

    def add(self, new_datum: T) -> None:
        index = self.get_free_index()
        new_datum.index = index
        # todo check for conflicting names and aliases
        self.data[new_datum.index] = new_datum
        self.save()

    def add_alias(self, alias: str, index: int = None, name: str = None):
        datum: Optional[T] = None
        if index is not None:
            datum = self.data[index]
        elif name is not None:
            datum = self.find(name)
        if datum is None:
            raise KeyError()
        if alias not in datum.aliases:
            datum.aliases.append(alias)
        self.save()  # todo make sure it works (modifies self.data)

    def save(self):
        create_directory("db/data")
        with open(
            f"db/data/{self.get_data_type_name()}.json", mode="w"
        ) as current_file:
            current_file.write(
                json.dumps([datum.to_dict() for datum in self.data.values()])
            )
