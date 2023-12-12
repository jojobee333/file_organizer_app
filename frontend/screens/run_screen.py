import asyncio
import logging
import flet as ft

from backend.service import Service
from frontend.components.components import Title, ScreenContainer, Selector, secondary_color
from frontend.controllers.screen_controller import ScreenController
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class RunScreen(ft.UserControl):
    def __init__(self, col, screen_controller: ScreenController):
        super().__init__()
        self.target_text = None
        self.progress = None
        self.status_text = None
        self.folder_container = None
        self.run_btn = None
        self.origin_dropdown = None
        self.run_title = None
        self.controller = screen_controller
        self.screen_container = None
        self.main_column = None
        self.format_title = None
        self.all_origins = None
        self.all_targets = None
        self.all_formats = None
        self.property_column = None
        self.title_divider = ft.Divider(thickness=0.0, height=1, color=ft.colors.WHITE)
        self.col = col
        self.screen_type = "run"

    def get_data(self):
        self.all_targets = Service().get_all_targets()["results"]
        self.all_formats = Service().get_all_formats()["results"]
        self.all_origins = Service().get_all_origins()["results"]

    async def clear_page(self, e):
        self.screen_container.controls.clear()

    @staticmethod
    def populate_origins(origin_name: str, origin_id: int):
        return ft.dropdown.Option(text=origin_name, key=origin_id)

    async def move(self, origin_id):
        if origin_id:
            id = int(origin_id)
            origin_path = self.controller.get_origin_by_id(id)["path"]
            response = self.controller.move_files(origin_id=id, origin_path=origin_path)
            message = "\n".join(response["message"])
            await self.make_progress(message=message)
            logger.info(response)

    async def make_progress(self, message):
        self.status_text.value = message
        for i in range(0, 1):
            self.progress.value = i * 1
            logger.info(self.progress.value)
            await asyncio.sleep(0.1)
            await self.update_async()

    def get_components(self):
        self.run_title = Title("Run", col=11)
        self.main_column = ft.SafeArea(
            col=12,
            minimum=10,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                col=12,
                controls=[
                    Title("Run"),
                    self.title_divider
                ]))

        origin_options = [RunScreen.populate_origins(origin_name=origin["name"], origin_id=origin["id"])
                          for origin in self.all_origins]
        self.target_text = ft.Column(col=3,
                                     controls=[ft.TextButton(icon=ft.icons.FOLDER,
                                                             text=target["name"],
                                                             style=ft.ButtonStyle(color=ft.colors.WHITE,
                                                                                  shape=ft.RoundedRectangleBorder(
                                                                                      radius=5))) for target in
                                               self.all_targets])

        self.origin_dropdown = Selector(col=12, options=origin_options, hint_text="Choose Origin")
        self.run_btn = ft.TextButton(text="Run",
                                     on_click=lambda e: asyncio.create_task(self.move(
                                         origin_id=self.origin_dropdown.value)),
                                     style=ft.ButtonStyle(color=ft.colors.WHITE,
                                                          bgcolor=secondary_color,
                                                          shape=ft.RoundedRectangleBorder(
                                                              radius=5)))
        self.folder_container = ft.Container(col=3,
                                             content=ft.Column(controls=[ft.Icon(ft.icons.FOLDER, size=200, col=12),
                                                                         self.origin_dropdown]))
        self.status_text = ft.Text()
        self.progress = ft.ProgressBar(bar_height=15, value=1)

    def build(self):
        self.get_data()
        self.get_components()

        return ScreenContainer(
            content=ft.SafeArea(
                minimum=30,
                content=ft.ResponsiveRow(
                    col=12,
                    controls=[
                        self.run_title,
                        self.title_divider,
                        self.folder_container,
                        ft.SafeArea(
                            minimum=50,
                            col=6,
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    self.status_text,
                                    self.progress
                                ]),

                        ),
                        self.target_text,
                        self.run_btn

                    ]
                )))
