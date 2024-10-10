from functions.querying.View import View
from functions.querying.standard_columns import (
    ORDINAL,
    LENGTH,
    standard,
    ERRORS,
    WARNINGS,
)

STANDARD_VIEW = View(
    [
        ORDINAL,
        LENGTH,
        standard("artists", 70),
        standard("title", 30),
    ]
)

ANALYZE_VIEW = View(
    [
        ORDINAL,
        LENGTH,
        standard("artists", 70),
        standard("title", 30),
        ERRORS,
        WARNINGS,
    ]
)
