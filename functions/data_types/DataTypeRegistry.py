import json
from typing import Optional, Dict
from typing import TypeVar, Generic

from functions.data_types.DataType import DataType
from libs.io import create_directory
from libs.strings import quoted

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
        name_lower = name.lower()
        for datum in self.data.values():
            if datum.name.lower() == name_lower:
                return datum
            for alias in datum.aliases:
                if alias.lower() == name_lower:
                    return datum
            for alias in datum.misspellings:
                if alias.lower() == name_lower:
                    return datum

    def add(self, new_datum: T) -> None:
        index = self.get_free_index()
        new_datum.index = index
        self.check_repeated(new_datum)
        self.check_specific(new_datum)
        self.data[new_datum.index] = new_datum
        self.save()

    def add_variant(self, name: str, variant: str, alias: bool, force: bool = False) -> None:
        datum = self.find(name)
        if not datum:
            raise KeyError(f"Could not find {self.get_data_type_name()} by {quoted(name)}")

        used = self.find(variant)
        if used:
            if variant == used.name:
                # todo if force, say it's impossible
                raise KeyError(f"{quoted(name)} is an existing {self.get_data_type_name()}")
            if variant in used.aliases:
                # todo if force, remove the other usage first
                raise KeyError(f"{quoted(name)} already used as an alias for {quoted(used.name)}")
            else:
                # todo if force, remove the other usage first
                raise KeyError(f"{quoted(name)} already used as a misspelling for {quoted(used.name)}")

        if alias:
            datum.aliases.append(variant)
        else:
            datum.misspellings.append(variant)
        self.save()

    def add_alias(self, name: str, alias: str, force: bool = False) -> None:
        self.add_variant(name, alias, True, force)

    def add_misspelling(self, name: str, alias: str, force: bool = False) -> None:
        self.add_variant(name, alias, False, force)

    def check_repeated(self, new_datum: T) -> None:
        repeated_names = []
        for alias in [new_datum.name] + new_datum.aliases:
            if self.find(alias) is not None:
                repeated_names.append(alias)
        if len(repeated_names):
            raise KeyError(
                f"The following name{'(s) are' if len(repeated_names) > 1 else ' is'} "
                f" already used: {', '.join(repeated_names)}")

    def check_specific(self, new_datum: T) -> None:
        return

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
