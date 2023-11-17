import flet as ft
from flet_core import border_radius

from constants import SMALL_PADDING, RADIUS


class TargetCard(ft.Container):
    def __init__(self, items: list, color):
        super().__init__()
        self.items = items
        self.content = ft.Column(controls=items)
        self.padding = SMALL_PADDING
        self.border_radius = border_radius.all(RADIUS)
        self.col = 3
        self.bgcolor = color






