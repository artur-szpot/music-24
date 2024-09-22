import shutil
from enum import Enum
from math import ceil
from typing import Optional

from functions.lines.Line import Line, LineElement
from functions.settings.AppSettings import PAGE_SIZE_AUTO
from functions.settings.app_settings import app_settings
from functions.settings.text_color.SchemeColor import SchemeColor


class TerminalSizeError(ValueError):
    pass


class HeaderType(Enum):
    NONE = 0
    SIMPLE_PAGINATION = 1
    TABLE_HEADER = 3


class CurrentPosition:
    page_number = 0
    total_items = 0
    total_pages = 0
    first_item = 0
    last_item = 0
    page_size = 1
    max_width = 80
    terminal_size = 10
    header_type = HeaderType.NONE

    def new_result(
        self, total_items: int, header_type: Optional[HeaderType] = None
    ) -> None:
        self.page_number = 0
        self.total_items = total_items
        self.header_type = header_type or self.header_type
        self.update()

    def update_pages(self):
        self.total_pages = ceil(self.total_items / self.page_size)

    def render_pagination(self) -> Optional[Line]:
        self.first_item = self.page_number * self.page_size
        self.last_item = min((self.page_number + 1) * self.page_size, self.total_items)
        if self.header_type == HeaderType.SIMPLE_PAGINATION:
            return self.render_simple_pagination()
        elif self.header_type == HeaderType.TABLE_HEADER:
            return self.render_table_pagination()
        return None

    def render_simple_pagination(self) -> Line:
        return Line(
            [
                LineElement(" (page "),
                LineElement.bold(self.page_number + 1),
                LineElement(" of "),
                LineElement.bold(self.total_pages),
                LineElement(")"),
            ],
            color=SchemeColor.INFO,
        )

    def render_table_pagination(self) -> Line:
        return Line(
            [
                LineElement("Items "),
                LineElement.bold(self.first_item + 1),
                LineElement(" to "),
                LineElement.bold(self.last_item),
                LineElement(" of "),
                LineElement.bold(self.total_items),
                LineElement(" - page "),
                LineElement.bold(self.page_number + 1),
                LineElement(" of "),
                LineElement.bold(self.total_pages),
            ],
            color=SchemeColor.INFO,
        )

    def set_page_size(self, page_size: int) -> None:
        app_settings.set("page_size", page_size)
        self.new_result(self.total_items)

    def update(self) -> None:
        terminal_size = shutil.get_terminal_size()
        self.max_width = terminal_size.columns
        if app_settings.page_size == PAGE_SIZE_AUTO:
            self.terminal_size = terminal_size.lines
        else:
            self.terminal_size = min(app_settings.page_size, terminal_size.lines)
        # 3 for last command/message, break, pagination
        # 1 or 3 for table header
        # 2 for break, input
        pagination_size = 1
        if (
            not app_settings.compact_table_header
            and self.header_type == HeaderType.TABLE_HEADER
        ):
            pagination_size = 3
        self.page_size = self.terminal_size - 3 - pagination_size - 2
        if self.page_size < 2:
            raise TerminalSizeError(
                "Terminal is too small to display the application. Increase terminal height or enable compact table "
                f"headers. Terminal size: {self.terminal_size}, page size: {self.page_size}"
            )
        self.update_pages()
