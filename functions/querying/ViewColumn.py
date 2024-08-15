from typing import Dict, Optional

from functions.querying.SpecialColumn import SpecialColumn


class ViewColumn:
    label: str
    width: int
    property_name: Optional[str]
    right_align: bool
    special: Optional[SpecialColumn]

    def __init__(self, source: Dict):
        self.label = source.get("label")
        if not self.label:
            raise ValueError("Missing label")
        self.width = source.get("width")
        if not self.width:
            raise ValueError("Missing width")
        self.property_name = source.get("property_name")
        self.special = source.get("special")
        if not self.property_name and self.special is None:
            raise ValueError(
                "Either property name or special needs to be set in a ViewColumn"
            )
        self.right_align = source.get("right_align", False)

    def to_dict(self) -> Dict:
        return {
            "label": self.label,
            "width": self.width,
            "property_name": self.property_name,
            "right_align": self.right_align,
            "special": self.special.value,
        }
