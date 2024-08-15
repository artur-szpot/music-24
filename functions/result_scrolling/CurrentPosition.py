from math import ceil

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

    def render(self) -> str:
        self.first_item = self.page_number * app_settings.page_size
        self.last_item = min(
            (self.page_number + 1) * app_settings.page_size, self.total_items
        )
        return f"Items {self.first_item + 1} to {self.last_item} of {self.total_items} - page {self.page_number + 1} of {self.total_pages}"

    def set_page_size(self, page_size: int) -> None:
        app_settings.set("page_size", page_size)
        self.new_result(self.total_items)
