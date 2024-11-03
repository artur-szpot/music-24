from functions.querying.SpecialColumn import SpecialColumn
from functions.querying.ViewColumn import ViewColumn

ORDINAL = ViewColumn(
    label="no.",
    width=6,
    right_align=True,
    special=SpecialColumn.ORDINAL_NUMBER,
)

LENGTH = ViewColumn(
    label="length",
    width=8,
    right_align=True,
    special=SpecialColumn.LENGTH,
)

ERRORS = ViewColumn(
    label="errors",
    width=7,
    right_align=True,
    special=SpecialColumn.ERRORS,
)

WARNINGS = ViewColumn(
    label="warnings",
    width=9,
    right_align=True,
    special=SpecialColumn.WARNINGS,
)


def standard(name: str, width: int, property_name: str = None) -> ViewColumn:
    return ViewColumn(label=name, width=width, property_name=property_name or name)
