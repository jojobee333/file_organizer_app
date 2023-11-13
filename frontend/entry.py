import json
import logging

import flet as ft
from flet_core import FilePickerResultEvent
import requests
from constants import HEIGHT, url_base, SIZE, HEADERS
from frontend.format_module import FormatControl
from frontend.origin_module import OriginControl
from frontend.target_module import TargetControl

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


def main(page: ft.Page):

    # hide all dialogs in overlay
    page.add(
        ft.ResponsiveRow(
            controls=[OriginControl(),
                      TargetControl(),
                      FormatControl()]
        ),

    )


ft.app(target=main)

# origin_text_field,
# choose_new_folder_btn,
# add_origin_btn
