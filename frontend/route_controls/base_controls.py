import flet as ft
from flet_core import border_radius

from constants import ROW_HEIGHT, LARGE_SIZE, SMALL_PADDING, RADIUS, LARGE_PADDING


class TargetCard(ft.Container):
    def __init__(self, items: list, color):
        super().__init__()
        self.items = items
        self.content = ft.ResponsiveRow(controls=items)
        self.padding = LARGE_PADDING
        self.border_radius = border_radius.all(RADIUS)
        self.col = 2
        self.bgcolor = color


class Title(ft.Text):

    def __init__(self, value, col):
        super().__init__()
        self.value = value
        self.height = ROW_HEIGHT
        self.col = col
        self.weight = ft.FontWeight.BOLD
        self.size = LARGE_SIZE


class AddButton(ft.IconButton):
    def __init__(self, col, on_click):
        super().__init__()
        self.col = col
        self.icon = ft.icons.ADD
        self.height = ROW_HEIGHT
        self.on_click = on_click
        self.style = ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=RADIUS)
        )


class CustomElevatedButton(ft.ElevatedButton):
    def __init__(self, text, col, on_click, icon):
        super().__init__()
        self.text = text
        self.col = col
        self.icon = icon
        self.height = ROW_HEIGHT
        self.on_click = on_click
        self.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=RADIUS))


class CustomField(ft.TextField):
    def __init__(self, col: int, hint_text: str, disabled: bool):
        super().__init__()
        self.hint_text = hint_text
        self.content_padding = SMALL_PADDING
        self.col = col
        self.filled = True
        self.disabled = disabled
        self.border_radius = ft.border_radius.all(RADIUS)
        self.height = ROW_HEIGHT
        self.text_size = LARGE_SIZE
