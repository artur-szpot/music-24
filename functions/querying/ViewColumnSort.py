from typing import Dict


class ViewColumnSort:
    property_name: str = ""
    ascending: bool = True

    def __init__(self, property_name: str, ascending: bool = True):
        self.property_name = property_name
        self.ascending = ascending

    def to_dict(self) -> Dict:
        return {"property_name": self.property_name, "ascending": self.ascending}
