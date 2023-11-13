import json
import logging
import flet as ft
import requests
from flet_core import FilePickerResultEvent, MainAxisAlignment

from constants import HEADERS, url_base, HEIGHT
from frontend.custom_target_card import TargetCard

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

    def __init__(self):
        super().__init__()

    def build(self):
        def get_directory_result(e: FilePickerResultEvent):
            target_path = e.path if e.path else ""
            if target_path:
                new_destination_card(target_path)
            self.update()

        def new_destination_card(target_path):
            target_grid.controls.append(
                TargetCard(
                    color=CARD_COLOR,
                    items=[
                        target_folder_icon,
                        ft.ResponsiveRow(controls=[name_to_add, submit_btn]),
                        ft.Text(target_path, size=SMALL_SIZE, no_wrap=True, max_lines=1)]))

        def submit_final_card(e):
            """Submit the target card and add target to database."""
            label = name_to_add.value
            items = target_grid.controls[-1].items
            path = items[-1].value
            items.remove(target_grid.controls[-1].items[1])
            items.insert(1, ft.Text(label, size=LARGE_SIZE, weight=ft.FontWeight.BOLD))
            json.loads(requests.post(headers=HEADERS, url=f"{url_base}/targets/?name={label}&path={path}").text)
            self.update()

        name_to_add = ft.TextField(col=8, hint_text="Add Label", height=HEIGHT, autofocus=True)
        submit_btn = ft.IconButton(col=4, icon=ft.icons.CHECK, on_click=submit_final_card)
        all_targets = json.loads(requests.get(headers=HEADERS, url=f"{url_base}/targets/").text)
        target_folder_icon = ft.Icon(ft.icons.FOLDER, size=100)
        target_grid = ft.ResponsiveRow(
            controls=[
                TargetCard(
                    color=CARD_COLOR,
                    items=[
                        target_folder_icon,
                        ft.Text(item["name"], size=LARGE_SIZE, weight=ft.FontWeight.BOLD),
                        ft.Text(item["path"], size=SMALL_SIZE, no_wrap=True, max_lines=1)
                    ]

                ) for item in all_targets["results"]])

        title = ft.Text("Destination Folders", col=9, height=HEIGHT, size=LARGE_SIZE)
        choose_new_dest_btn = ft.ElevatedButton("New Destination", col=3, icon=ft.icons.FOLDER_OPEN, height=HEIGHT,
                                                on_click=lambda _: get_target_directory_dialog.get_directory_path(),
                                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)))

        get_target_directory_dialog = ft.FilePicker(on_result=get_directory_result)
        return ft.ResponsiveRow(
            controls=[
                title,
                choose_new_dest_btn,
                get_target_directory_dialog,
                target_grid]
        )
