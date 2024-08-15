from functions.querying.SpecialColumn import SpecialColumn
from functions.querying.ViewColumn import ViewColumn

ORDINAL = ViewColumn(
    {
        "label": "no.",
        "width": 6,
        "right_align": True,
        "special": SpecialColumn.ORDINAL_NUMBER,
    }
)

LENGTH = ViewColumn(
    {
        "label": "length",
        "width": 8,
        "right_align": True,
        "special": SpecialColumn.LENGTH,
    }
)


ERRORS = ViewColumn(
    {
        "label": "errors",
        "width": 7,
        "right_align": True,
        "special": SpecialColumn.ERRORS,
    }
)


def standard(name: str, width: int, label: str = None) -> ViewColumn:
    return ViewColumn({"label": name, "width": width, "property_name": label or name})
