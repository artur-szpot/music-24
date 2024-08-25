from math import ceil

from functions.execute.Line import Line, LineElement
from functions.settings.app_settings import app_settings


class CurrentPosition:
    page_number = 0
    total_items = 0
    total_pages = 0
    first_item = 0
    last_item = 0

    def new_result(self, total_items: int) -> None:
        self.page_number = 0
        self.total_items = total_items
        self.total_pages = ceil(self.total_items / app_settings.page_size)

    def render(self) -> Line:
        self.first_item = self.page_number * app_settings.page_size
        self.last_item = min(
            (self.page_number + 1) * app_settings.page_size, self.total_items
        )
        return Line([
            LineElement("Items "),
            LineElement.bold(self.first_item + 1),
            LineElement(" to "),
            LineElement.bold(self.last_item),
            LineElement(" of "),
            LineElement.bold(self.total_items),
            LineElement(" - page "),
            LineElement.bold(self.page_number+1),
            LineElement(" of "),
            LineElement.bold(self.total_pages),
        ])

    def set_page_size(self, page_size: int) -> None:
        app_settings.set("page_size", page_size)
        self.new_result(self.total_items)
