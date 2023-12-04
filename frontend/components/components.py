from enum import Enum

import flet as ft

from constants import ROW_HEIGHT, TEXT_SIZE, SMALL_PADDING, RADIUS, MAX_HEIGHT, HEADING_ONE, LARGE_ICON, \
    SMALL_ICON, LARGEST_ICON, LARGE_PADDING


class Tag(Enum):
    NEW_ORIGIN = 1
    NEW_TARGET = 2
    NEW_FORMAT = 3


default_style = ft.TextStyle(
    size=TEXT_SIZE
)
transparent = ft.colors.with_opacity(0.0, '#ffffff')
primary_color = ft.colors.with_opacity(1.0, '#262626')
secondary_color = ft.colors.with_opacity(1.0, '#3A3A3A')
tertiary_color = ft.colors.with_opacity(1.0, '#4A494A')
primary_border_color = ft.colors.with_opacity(1.0, '#A7A9AC')
primary_text_color = ft.colors.with_opacity(1.0, '#A7A9AC')
default_folder_color = ft.colors.with_opacity(1.0, '#FFD770')
blue_folder_color = ft.colors.with_opacity(1.0, '#84B3E0')


class Title(ft.Text):
    def __init__(self, value, col=12):
        super().__init__()
        self.col = col
        self.value = value
        self.weight = ft.FontWeight.BOLD


class CloseButton(ft.IconButton):
    def __init__(self, col: int, on_click):
        super().__init__()
        self.icon = ft.icons.CLOSE
        self.col = col
        self.height = 20
        self.icon_size = 12
        self.on_click = on_click


class OKButton(ft.TextButton):
    def __init__(self, on_click):
        super().__init__()
        self.text = "OK"
        self.style = ft.ButtonStyle(color=primary_text_color)
        self.on_click = on_click


class NavButton(ft.TextButton):
    def __init__(self, icon, text, on_click):
        super().__init__()
        self.text = text
        self.icon = icon
        self.style = ft.ButtonStyle(
            color=ft.colors.WHITE
        )
        self.on_click = on_click


class AddButton(ft.IconButton):
    def __init__(self, on_click, col=2):
        super().__init__()
        self.col = col
        self.on_click = on_click
        self.icon = ft.icons.ADD
        self.icon_size = 20
        self.height = ROW_HEIGHT
        self.style = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5))



class Selector(ft.Dropdown):
    def __init__(self, hint_text: str, options: list, col: int):
        super().__init__()
        self.autofocus = False
        self.height = ROW_HEIGHT
        self.content_padding = SMALL_PADDING
        self.alignment = ft.alignment.center_left
        self.dense = True
        self.filled = False
        self.border_color = transparent
        self.bgcolor = transparent
        self.focused_bgcolor = transparent
        self.text_size = TEXT_SIZE
        self.text_style = default_style
        self.hint_style = default_style
        self.alignment = ft.alignment.bottom_center
        self.hint_text = hint_text
        self.options = options
        self.col = col


class AlertBox(ft.AlertDialog):
    def __init__(self, title, tag: Tag, actions: list):
        super().__init__()
        self.tag = tag
        self.actions_padding = 20
        self.title = title
        self.font_family = "Gadugi"
        self.weight = ft.FontWeight.BOLD
        self.content_padding = LARGE_PADDING
        self.actions = [ft.Column(
            controls=actions)]


class PropertyColumn(ft.Container):
    def __init__(self, folder_name: str, path: str, format_section, delete_click):
        super().__init__()
        self.col = 3
        self.popup_button = ft.PopupMenuButton(
            height=25,
            col=2,
            scale=0.7,
            items=[
                ft.PopupMenuItem(text="Delete", on_click=delete_click)
            ]

        )
        self.padding = LARGE_PADDING
        self.bgcolor = primary_color
        self.border = ft.border.only(left=ft.border.BorderSide(1, primary_border_color))
        self.divider = ft.Divider(thickness=0.0, height=1, color=ft.colors.WHITE)
        self.title = Title("Properties", col=10)
        self.format_section = format_section
        self.content = ft.ResponsiveRow(
            controls=[
                ft.ResponsiveRow(
                    controls=[self.title, self.popup_button]),
                self.divider,
                ft.Row(col=12,
                       alignment=ft.MainAxisAlignment.CENTER,
                       controls=[ft.Icon(ft.icons.FOLDER, size=200)]),
                AlertField(value=folder_name, col=12, disabled=True, prefix=ft.Text("Name  "), height=ROW_HEIGHT),
                AlertField(value=path, col=12, disabled=True, height=ROW_HEIGHT, text_size=9),
                ft.Text("", col=12),
                ft.Divider(thickness=0.0, height=1, color=ft.colors.WHITE),
                self.format_section

            ])


class AlertField(ft.TextField):
    def __init__(self, col, disabled, value=None, hint_text=None, label=None, prefix=None, height=40, text_size=TEXT_SIZE):
        super().__init__()
        self.prefix = prefix
        self.prefix_style = ft.TextStyle(size=TEXT_SIZE, weight=ft.FontWeight.BOLD)
        self.value = value
        self.label = label
        self.text_size = text_size
        self.disabled = disabled
        self.hint_text = hint_text
        self.text_style = default_style
        self.col = col
        self.border_radius = ft.border_radius.all(RADIUS)
        self.bgcolor = secondary_color
        self.height = height


class ThemedField(ft.TextField):
    def __init__(self, col: int, disabled: bool, hint_text=None, value=None, prefix=None):
        super().__init__()
        self.prefix = prefix
        self.hint_text = hint_text
        self.value = value
        self.col = col
        self.disabled = disabled
        self.border = "none"
        self.bgcolor = transparent
        self.autofocus = False
        self.text_size = TEXT_SIZE
        self.text_style = default_style
        self.height = ROW_HEIGHT


class FolderContainer(ft.Container):
    def __init__(self, tag, folder_name: str, on_click=None,
                 color=default_folder_color):
        super().__init__()
        self.tag = tag
        self.folder_name = folder_name
        self.bgcolor = secondary_color
        self.padding = LARGE_PADDING
        self.border_radius = ft.border_radius.all(RADIUS)
        self.on_click = on_click
        self.content = ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[ft.SafeArea(
                content=ft.Container(
                    border_radius=ft.border_radius.all(RADIUS),
                    padding=ft.padding.symmetric(20, 40),
                    bgcolor=primary_color,
                    content=ft.Icon(ft.icons.FOLDER,
                                    size=LARGEST_ICON,
                                    color=color)
                )),
                ft.Row(controls=
                       [ft.Text(self.folder_name, width=125)])
            ]
        )


class DashboardContainer(ft.Container):
    def __init__(self, title: str, amount: int, unit: str, content: list, icon_type, on_click):
        super().__init__()
        self.bgcolor = secondary_color
        self.border_radius = ft.border_radius.all(RADIUS)
        self.title = ft.Text(title, weight=ft.FontWeight.BOLD, size=HEADING_ONE)
        self.amount = ft.Text(f"{amount} {unit}")
        self.icon_column = ft.Column(col=1,
                                     controls=[ft.IconButton(icon_type, icon_size=LARGE_ICON, on_click=on_click)])
        self.title_column = ft.Column(col=4, controls=[self.title, self.amount])
        self.content_column = ft.ListView(col=5, height=80, controls=content, spacing=5)
        self.content = ft.SafeArea(
            minimum=SMALL_PADDING,
            content=ft.ResponsiveRow(
                controls=[
                    ft.Container(col=4,
                                 padding=10,
                                 bgcolor=tertiary_color,
                                 content=ft.Row(
                                     controls=[
                                         self.icon_column,
                                         self.title_column])),
                    self.content_column

                ]
            ))


class BulletedItem(ft.Row):
    def __init__(self, item_name: str, icon_color=primary_border_color):
        super().__init__()
        self.controls = [ft.Icon(ft.icons.CIRCLE, color=icon_color, size=SMALL_ICON), ft.Text(item_name)]


class ListScroller(ft.ListView):
    def __init__(self, controls: list, height=70, horizontal=False):
        super().__init__()
        self.horizontal = horizontal
        self.height = height
        self.spacing = 5
        self.controls = controls


class SingleItemLogRow(ft.Container):
    def __init__(self, name: str, files_moved: int, date: str):
        super().__init__()
        self.col = 12
        self.padding = SMALL_PADDING
        self.bgcolor = tertiary_color
        self.border_radius = ft.border_radius.all(RADIUS)
        self.content = ft.ResponsiveRow(controls=[
            ft.Icon(ft.icons.CIRCLE, col=1),
            ft.Text(name, col=4),
            ft.Text(str(files_moved), col=6),
            ft.Text(date, col=1)
        ])
class SingleItemFileRow(ft.Container):
    def __init__(self, name: str, location: str, on_click=None):
        super().__init__()
        self.col = 12
        self.padding = SMALL_PADDING
        self.bgcolor = tertiary_color
        self.border_radius = ft.border_radius.all(RADIUS)
        self.content = ft.ResponsiveRow(controls=[
            ft.Icon(ft.icons.CIRCLE, col=1),
            ft.Text(name, col=7),
            ft.Text(location, col=4)
        ])


class SingleItemFormatRow(ft.Container):
    def __init__(self, name: str, location: str, on_click=None):
        super().__init__()
        self.col = 12
        self.padding = SMALL_PADDING
        self.bgcolor = tertiary_color
        self.border_radius = ft.border_radius.all(RADIUS)
        self.content = ft.ResponsiveRow(controls=[
            ft.Icon(ft.icons.CIRCLE, col=1),
            ft.Text(name, col=7),
            ft.Text(location, col=3),
            ft.IconButton(ft.icons.DELETE, on_click=on_click, col=1, height=20, icon_size=15)
        ])


class ScreenContainer(ft.Container):
    def __init__(self, content):
        super().__init__()
        self.col = 12
        self.height = MAX_HEIGHT
        self.margin = ft.margin.symmetric(vertical=-5, horizontal=-10)
        self.padding = ft.padding.symmetric(vertical=5, horizontal=10)
        self.bgcolor = primary_color
        self.content = content


class SecondaryContainer(ft.Container):
    def __init__(self, col, content):
        super().__init__()
        self.col = col
        self.height = ROW_HEIGHT
        self.bgcolor = primary_color
        self.border = ft.border.all(1, primary_border_color)
        self.border_radius = ft.border_radius.all(RADIUS)
        self.content = content
