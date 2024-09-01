import shutil
from math import ceil

from functions.lines.Line import Line, LineElement
from functions.lines.SchemeColor import SchemeColor
from functions.settings.app_settings import app_settings


class CurrentPosition:
    page_number = 0
    total_items = 0
    total_pages = 0
    first_item = 0
    last_item = 0
    page_size = 1

    def new_result(self, total_items: int) -> None:
        self.page_number = 0
        self.total_items = total_items
        self.total_pages = ceil(self.total_items / self.page_size)

    def render_page_header(self) -> Line:
        self.first_item = self.page_number * self.page_size
        self.last_item = min((self.page_number + 1) * self.page_size, self.total_items)
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

    def render_table_header(self) -> Line:
        self.first_item = self.page_number * self.page_size
        self.last_item = min((self.page_number + 1) * self.page_size, self.total_items)
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
        self.page_size = min(app_settings.page_size, terminal_size.lines)
