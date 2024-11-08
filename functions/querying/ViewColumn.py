from typing import Dict, Optional

from functions.querying.SpecialColumn import SpecialColumn


class ViewColumn:
    label: str
    width: int
    property_name: Optional[str]
    right_align: bool
    special: Optional[SpecialColumn]

    def __init__(
        self,
        label: str,
        width: int,
        property_name: Optional[str] = None,
        right_align: bool = False,
        special: Optional[SpecialColumn] = None,
    ):
        self.label = label
        self.width = width
        self.property_name = property_name
        self.special = special
        if not self.property_name and self.special is None:
            raise ValueError(
                "Either property name or special needs to be set in a ViewColumn"
            )
        self.right_align = right_align

    @staticmethod
    def from_dict(source: Dict):
        return ViewColumn(
            label=source.get("label"),
            width=source.get("width"),
            property_name=source.get("property_name"),
            special=source.get("special"),
            right_align=source.get("right_align"),
        )

    def to_dict(self) -> Dict:
        return {
            "label": self.label,
            "width": self.width,
            "property_name": self.property_name,
            "right_align": self.right_align,
            "special": self.special.value,
        }
