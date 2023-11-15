import json
import logging
import flet as ft
import requests
from flet_core import FilePickerResultEvent

from constants import url_base, HEADERS

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class FormatControl(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        all_formats = json.loads(requests.get(headers=HEADERS, url=f"{url_base}/formats/").text)
        logging.info(all_formats)
        return ft.ResponsiveRow(
            controls=[ft.ElevatedButton(
                text="Add New Formats",
                icon=ft.icons.ADD)]
        )
