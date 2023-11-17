import flet as ft

from constants import ROW_HEIGHT


class FormatCard(ft.Container):
    def __init__(self, items):
        super().__init__()
        self.items = items
        self.col = 12
        self.height = ROW_HEIGHT
        self.padding = 5
        self.bgcolor = ft.colors.GREY_900
        self.border_radius = ft.border_radius.all(5)
        self.content = ft.ResponsiveRow(items)
