import flet as ft
from backend.service import Service
from frontend.components.components import ScreenContainer


class BaseScreen(ft.UserControl):

    def __init__(self, screen_type):
        super().__init__()
        self.col = 10
        self.screen_type = screen_type
        self.controls = ft.Text("")
        self.all_formats = None
        self.all_targets = None
        self.all_origins = None
        self.padding = 10
        self.main = ft.Column(
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=self.controls,
            col=12,
        )
        self.screen_frame = ScreenContainer(
            content=ft.SafeArea(
                minimum=self.padding,
                content=self.main
            ))

    @staticmethod
    def get_data():
        formats = Service.get_all_formats()
        targets = Service.get_all_targets()
        folders = Service.get_all_origins()
        return formats, targets, folders

    def build(self):
        return self.screen_frame
