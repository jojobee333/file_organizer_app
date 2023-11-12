import logging

import flet as ft
from flet_core import FilePickerResultEvent
import requests
from constants import HEIGHT, SIZE

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


def main(page: ft.Page):
    # Pick files dialog

    # Open directory dialog
    def get_directory_result(e: FilePickerResultEvent):
        origin_text_field.value = e.path if e.path else ""
        origin_text_field.update()

    def add_origin():
        if not origin_text_field.value == "":
            logger.info(origin_text_field.value)
            requests.post(f"http://127.0.0.1:8000/origins/", data={"path": str(origin_text_field.value)})

    get_directory_dialog = ft.FilePicker(on_result=get_directory_result)

    origin_text_field = ft.TextField(col=9,
                                     filled=True,
                                     border_radius=ft.border_radius.all(5),
                                     height=HEIGHT,
                                     text_size=SIZE)

    # hide all dialogs in overlay
    page.overlay.extend([get_directory_dialog])

    page.add(
        ft.ResponsiveRow(
            [origin_text_field,
             ft.ElevatedButton(
                 "Choose New Folder",
                 col=2,
                 icon=ft.icons.FOLDER_OPEN,
                 height=HEIGHT,
                 on_click=lambda _: get_directory_dialog.get_directory_path(),
                 disabled=page.web,
                 style=ft.ButtonStyle(
                     shape=ft.RoundedRectangleBorder(radius=5)
                 )
             ),
             ft.IconButton(
                 col=1,
                 icon=ft.icons.ADD,
                 height=HEIGHT,
                 on_click=lambda _: add_origin(),
                 disabled=page.web,
                 style=ft.ButtonStyle(
                     shape=ft.RoundedRectangleBorder(radius=5)
                 )
             ),

             ]
        ),
    )


ft.app(target=main)
