import asyncio
import logging

import flet as ft
from flet_core import ElevatedButton

from constants import ROW_HEIGHT, LARGE_SIZE
from frontend.route_controls.alert_controls.alert_handler import AlertHandler
from frontend.route_controls.base_controls import CustomElevatedButton
from frontend.exceptions.custom_exceptions import InvalidEntryException
from frontend.service import Service

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class SideBar(ft.UserControl):
    def __init__(self, col,
                 refresh_button: ElevatedButton):
        super().__init__()
        self.select_origin = None
        self.col = col
        self.refresh_button = refresh_button
        self.move_button = None
        self.logo = None

    async def alert_handler(self, title, message):
        async def close_button_handler(e):
            asyncio.create_task(AlertHandler.close_alert(e=e, page=self.page, alert=alert))

        alert = ft.AlertDialog(title=ft.Text(title),
                               content=ft.Text(message),
                               actions=[ft.TextButton("OK", on_click=close_button_handler)])
        await AlertHandler.open_alert(self.page, alert)

    async def move(self, e):
        logger.info("Hello")
        try:
            if self.select_origin.value:
                origin_id = Service.get_origin_by_path(self.select_origin.value)["id"]
                logger.info(origin_id)
                response = Service.move_files(origin_path=self.select_origin.value, origin_id=origin_id)
                message = "\n".join(response["message"])
                await self.alert_handler(title="Summary", message=message)
            else:
                raise InvalidEntryException("Origin is not valid")
        except Exception as e:
            logger.info(e)
            await self.alert_handler(title="Invalid Origin", message="The origin path is not valid.")

    def build(self):
        self.move_button = CustomElevatedButton(col=12, icon=ft.icons.PLAY_ARROW, text="Move", on_click=self.move)
        self.select_origin = ft.Dropdown(col=12,
                                         height=ROW_HEIGHT,
                                         hint_text="Choose Origin",
                                         text_size=LARGE_SIZE,
                                         options=[
                                             ft.dropdown.Option(f"{item['path']}") for item in
                                             Service.get_all_origins()["results"]
                                         ])

        self.logo = ft.Image(
            src="/frontend/assets/file_logo.png"
        )

        return ft.Container(
            expand=True,
            col=self.col,
            content=ft.ResponsiveRow(
                controls=[
                    self.logo,
                    self.refresh_button,
                    self.select_origin,
                    self.move_button
                ]

            ))
