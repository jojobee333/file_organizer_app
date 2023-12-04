import asyncio
import logging

import flet as ft

from backend.service import Service
from frontend.components.components import Title, ScreenContainer
from frontend.controllers.screen_controller import ScreenController

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class RunScreen(ft.UserControl):
    def __init__(self, col, screen_controller: ScreenController):
        super().__init__()
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

    def build(self):
        self.get_data()
        self.get_components()

        return ScreenContainer(content= ft.SafeArea(
                minimum=10,
                content=ft.Column(
                    scroll=ft.ScrollMode.ALWAYS,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    col=12,
                    controls=[
                        self.run_title,
                        self.title_divider,
                    ])))
