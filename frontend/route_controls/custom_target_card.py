import flet as ft
from flet_core import border_radius


class TargetCard(ft.Container):
    def __init__(self, items: list, color):
        super().__init__()
        self.items = items
        self.content = ft.Column(controls=items)
        self.padding = 10
        self.border_radius = border_radius.all(5)
        self.col = 3
        self.bgcolor = color






