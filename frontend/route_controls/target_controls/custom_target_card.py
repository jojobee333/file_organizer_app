import flet as ft
from flet_core import border_radius

from constants import RADIUS, LARGE_PADDING


class TargetCard(ft.Container):
    def __init__(self, items: list, color):
        super().__init__()
        self.items = items
        self.content = ft.ResponsiveRow(controls=items)
        self.padding = LARGE_PADDING
        self.border_radius = border_radius.all(RADIUS)
        self.col = 2
        self.bgcolor = color






