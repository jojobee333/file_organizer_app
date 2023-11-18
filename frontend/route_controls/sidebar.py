import flet as ft
from flet_core import IconButton, ElevatedButton, Dropdown

from constants import ROW_HEIGHT, LARGE_SIZE
from frontend.route_controls.base_controls import CustomField
from frontend.route_controls.service import Service


class SideBar(ft.UserControl):
    def __init__(self, col,
                 refresh_button: ElevatedButton,
                 move_button: ElevatedButton,
                 origin_dropdown: Dropdown):
        super().__init__()
        self.col = col
        self.refresh_button = refresh_button
        self.move_button = move_button
        self.select_origin = origin_dropdown

    def build(self):
        return ft.Container(
            expand=True,
            col=self.col,
            content=ft.ResponsiveRow(
                controls=[
                    self.refresh_button,
                    self.select_origin,
                    self.move_button
                ]

            ))
