import flet as ft

from constants import MAX_HEIGHT, LARGE_PADDING
from frontend.components.components import primary_border_color, NavButton


class LeftBar(ft.UserControl):
    def __init__(self, col, run_btn, schedule_btn, format_btn, folder_btn, dashboard_btn):
        super().__init__()
        self.run_btn = run_btn
        self.schedule_btn = schedule_btn
        self.format_btn = format_btn
        self.folder_btn = folder_btn
        self.dashboard_btn = dashboard_btn
        self.col = col

    def build(self):

        nav_container = ft.Container(
            height=MAX_HEIGHT,
            border=ft.border.only(right=ft.BorderSide(1, primary_border_color)),
            padding=LARGE_PADDING,
            expand=True,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                controls=[
                    self.dashboard_btn,
                    self.folder_btn,
                    self.format_btn,
                    self.schedule_btn,
                    self.run_btn
                ]
            ))

        return nav_container
