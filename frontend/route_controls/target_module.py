import json
import logging
import flet as ft
import requests
from flet_core import FilePickerResultEvent

from constants import HEADERS, url_base, HEIGHT
from frontend.route_controls.custom_target_card import TargetCard

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)

MAX_HEIGHT = 250
MAX_EXTENT = 220
PADDING = 5
LARGE_PADDING = 10
SMALL_SIZE = 10
LARGE_SIZE = 15
CARD_COLOR = ft.colors.GREY_900


class TargetControl(ft.UserControl):
    # OK

    def __init__(self):
        super().__init__()
        self.target_name_field = None
        self.all_targets = None
        self.target_folder_icon = None
        self.target_grid = None
        self.get_target_directory = None
        self.section_title = None
        self.choose_dest_button = None
        self.submit_button = None

    async def get_directory_result(self, e: FilePickerResultEvent):
        target_path = e.path if e.path else ""
        if target_path:
            self.new_destination_card(target_path)
        await self.update_async()

    def new_destination_card(self, target_path):
        self.target_grid.controls.append(
            TargetCard(
                color=CARD_COLOR,
                items=[
                    self.target_folder_icon,
                    ft.ResponsiveRow(controls=[self.target_name_field, self.submit_button]),
                    ft.Text(target_path, size=SMALL_SIZE, no_wrap=True, max_lines=1)]))

    async def submit_final_card(self, e):
        """Submit the target card and add target to database."""
        label = self.target_name_field.value
        items = self.target_grid.controls[-1].items
        path = items[-1].value
        items.remove(self.target_grid.controls[-1].items[1])
        items.insert(1, ft.Text(label, size=LARGE_SIZE, weight=ft.FontWeight.BOLD))
        json.loads(requests.post(headers=HEADERS, url=f"{url_base}/targets/?name={label}&path={path}").text)
        await self.update_async()

    def build(self):
        all_targets = json.loads(requests.get(headers=HEADERS, url=f"{url_base}/targets/").text)
        self.target_name_field = ft.TextField(col=8, hint_text="Add Label", height=HEIGHT, autofocus=True)
        self.submit_button = ft.IconButton(col=4, icon=ft.icons.CHECK, on_click=self.submit_final_card)
        self.target_folder_icon = ft.Icon(ft.icons.FOLDER, size=100)
        self.target_grid = ft.ResponsiveRow(
            controls=[
                TargetCard(
                    color=CARD_COLOR,
                    items=[
                        self.target_folder_icon,
                        ft.Text(item["name"], size=LARGE_SIZE, weight=ft.FontWeight.BOLD),
                        ft.Text(item["path"], size=SMALL_SIZE, no_wrap=True, max_lines=1)
                    ]

                ) for item in all_targets["results"]])
        self.get_target_directory = ft.FilePicker(on_result=self.get_directory_result)
        self.section_title = ft.Text("Destination Folders", col=9, height=HEIGHT, size=LARGE_SIZE)
        self.choose_dest_button = ft.ElevatedButton("New Destination", col=3, icon=ft.icons.FOLDER_OPEN, height=HEIGHT,
                                                    on_click=self.get_target_directory.get_directory_path_async,
                                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)))

        return ft.ResponsiveRow(
            controls=[
                self.section_title,
                self.choose_dest_button,
                self.get_target_directory,
                self.target_grid]
        )
