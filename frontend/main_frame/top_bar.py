import asyncio
import logging
import flet as ft
from flet_core import FilePickerResultEvent
from backend.service import Service
from constants import MIN_MODULE, ROW_HEIGHT
from frontend.components.components import (Selector, ThemedField, SecondaryContainer,
                                            primary_border_color, AlertField, AlertBox, Title, Tag, OKButton)
from frontend.control_handlers.alert_handler import AlertHandler

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class TopBar(ft.UserControl):
    def __init__(self, col):
        super().__init__()
        self.get_directory = None
        self.folder_dropdown = None
        self.folder_field = None
        self.alert = None
        self.col = col

    async def get_directory_result(self, e: FilePickerResultEvent):
        self.folder_field.value = e.path if e.path else ""
        await self.update_async()

    async def add_folder(self, folder_type, name, path, e):
        try:
            if folder_type == "Tag.NEW_ORIGIN":
                Service.add_origin(origin_name=name, origin_path=path)
            elif folder_type == "Tag.NEW_TARGET":
                Service.add_target(target_name=name, target_path=path)
            self.folder_field.value = ""
            await AlertHandler.close_alert(e=e, alert=self.alert, page=self.page)
        except Exception as e:
            logger.info(e)

    async def add_folder_alert(self, e):
        try:
            if not self.folder_field.value:
                raise ValueError("Empty Path Field")
            if not self.folder_dropdown.value:
                raise ValueError("No dropdown value is selected.")
            path = self.folder_field.value
            folder_type = self.folder_dropdown.value
            title_text = "New Origin" if folder_type == "Tag.NEW_ORIGIN" else "New Target"
            path_alert_field = ft.Text(value=path, col=12)
            name_alert_field = AlertField(value=path.split("\\")[-1], col=12, hint_text="Enter name for new origin.",
                                          disabled=False, label="Folder alias")
            logger.info(path)
            ok_button = OKButton(
                on_click=lambda e: asyncio.create_task(self.add_folder(folder_type=folder_type,
                                                                       name=name_alert_field.value,
                                                                       path=path, e=e)))

            self.alert = AlertBox(title=Title(title_text), actions=[path_alert_field, name_alert_field, ok_button],
                                  tag=folder_type)
            await AlertHandler.open_alert(alert=self.alert, page=self.page)
        except Exception as e:
            logger.info(f"Error occurred: {e}")

    def build(self):
        app_title = ft.SafeArea(
            col=2,
            minimum=15,
            content=ft.Text(
                "File Manager",
                height=ROW_HEIGHT,
                weight=ft.FontWeight.BOLD,
                text_align=ft.TextAlign.LEFT
            )
        )

        self.folder_field = ThemedField(col=11, disabled=True)
        self.get_directory = ft.FilePicker(on_result=self.get_directory_result)
        add_folder_button = ft.IconButton(
            ft.icons.ADD,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=20)
            ),
            icon_size=15,
            col=1,
            on_click=self.get_directory.get_directory_path_async
        )
        submit_button = ft.IconButton(ft.icons.CHECK, height=ROW_HEIGHT,
                                      icon_size=15,
                                      col=1,
                                      on_click=self.add_folder_alert)

        folder_field_container = SecondaryContainer(
            col=6,
            content=ft.ResponsiveRow(
                controls=[self.folder_field, add_folder_button]
            )
        )

        self.folder_dropdown = Selector(
            hint_text="Choose Folder Type",
            options=[ft.dropdown.Option(key=Tag.NEW_ORIGIN, text="Add Origin"),
                     ft.dropdown.Option(key=Tag.NEW_TARGET, text="Add Target")],
            col=2
        )

        return ft.Container(
            margin=-5,
            border=ft.border.only(bottom=ft.border.BorderSide(1, primary_border_color)),
            content=ft.ResponsiveRow(
                height=MIN_MODULE,
                controls=[
                    ft.Text("", col=12),
                    app_title,
                    folder_field_container,
                    submit_button,
                    self.folder_dropdown,
                    self.get_directory
                ]
            )
        )
