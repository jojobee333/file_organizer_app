import asyncio
import logging
import flet as ft
import flet_core
from flet_core import FilePickerResultEvent
from constants import ROW_HEIGHT, CARD_COLOR, LARGE_ICON, \
    RADIUS, LARGE_TXT, SMALL_TXT, MIN_MODULE
from frontend.exceptions.custom_exceptions import InvalidEntryException
from frontend.route_controls.alert_controls.alert_handler import AlertHandler
from frontend.route_controls.base_controls import Title, CustomField, TargetCard
from frontend.service.service import Service

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class TargetControl(ft.UserControl):
    # OK

    def __init__(self):
        super().__init__()
        self.target_name_field = None
        self.target_grid = None
        self.get_target_directory = None
        self.section_title = None
        self.choose_dest_button = None
        self.submit_button = None
        self.all_targets = Service.get_all_targets()
        self.all_formats = Service.get_all_formats()

    async def alert_handler(self):
        async def close_button_click(e):
            asyncio.create_task(AlertHandler.close_alert(e=e, page=self.page, alert=alert))

        alert = ft.AlertDialog(title=ft.Text("Invalid Name"),
                               content=ft.Text("The target name you entered is invalid."),
                               actions=[ft.TextButton("OK", on_click=close_button_click)])
        await AlertHandler.open_alert(self.page, alert)

    async def get_directory_result(self, e: FilePickerResultEvent):
        target_path = e.path if e.path else ""
        if target_path:
            self.new_destination_card(target_path)
        await self.update_async()

    def new_destination_card(self, target_path):
        try:
            self.target_grid.controls.append(
                TargetCard(
                    color=CARD_COLOR,
                    items=[
                        ft.Icon(ft.icons.FOLDER, size=LARGE_ICON, col=9),
                        ft.ResponsiveRow(controls=[self.target_name_field, self.submit_button]),
                        ft.Text(target_path, size=SMALL_TXT, no_wrap=True, max_lines=1)]))
        except Exception as e:
            logger.error(e)

    async def submit_target_card(self, e):
        """Submit the target card and add target to database."""
        try:
            if self.target_name_field.value:
                target_name = self.target_name_field.value
                items = self.target_grid.controls[-1].items
                path = items[-1].value
                response = Service.add_target(target_name=target_name, target_path=path)
                if response["code"] == 200:
                    new_target = Service.get_target_by_name(target_name)
                    for card in self.target_grid.controls:
                        if isinstance(card.items[1], flet_core.responsive_row.ResponsiveRow):
                            self.target_grid.controls.remove(card)
                            self.target_grid.controls.append(self.create_card(item=new_target))
                            await self.update_async()
            else:
                raise InvalidEntryException("No target name was found.")
        except InvalidEntryException as err:
            logger.info(err)
            await self.alert_handler()

    async def delete_target(self, e, target_id):
        target_to_delete = Service.get_target_by_id(target_id)
        response = Service.delete_target(target_id)
        if response.status_code == 200:
            await self.delete_destination_card(e, target_to_delete=target_to_delete)

    async def delete_destination_card(self, e, target_to_delete=None):
        for card in self.target_grid.controls:
            target_name = card.items[2].value
            if target_to_delete:
                if target_to_delete["name"] == target_name:
                    self.target_grid.controls.remove(card)
                    await self.update_async()
            else:
                self.target_grid.controls.remove(-1)

    def create_card(self, item):
        def delete_button_click(e):
            asyncio.create_task(self.delete_target(e, item["id"]))

        target_folder_icon = ft.Icon(ft.icons.FOLDER, size=LARGE_ICON, col=9)
        overflow_button = ft.PopupMenuButton(col=3, icon=ft.icons.MORE_VERT,
                                             items=[ft.PopupMenuItem(text="Delete", on_click=delete_button_click)
                                                    ])
        return TargetCard(
            color=CARD_COLOR,
            items=[

                target_folder_icon, overflow_button,
                ft.Text(item["name"], size=LARGE_TXT, weight=ft.FontWeight.BOLD),
                ft.Text(item["path"], size=SMALL_TXT, no_wrap=True, max_lines=1, overflow=ft.TextOverflow.FADE),
                ft.Row(controls=[ft.Container(
                    bgcolor=ft.colors.GREY_800,
                    padding=5,
                    border_radius=ft.border_radius.all(5),
                    content=ft.Text(fmt["name"], color="white"), col=1) for fmt in self.all_formats["results"] if
                    fmt["target_id"] == item["id"]])
            ])

    def build(self):
        self.section_title = Title(col=9, value="Destination Folders")
        self.get_target_directory = ft.FilePicker(on_result=self.get_directory_result)
        self.target_name_field = CustomField(col=8, hint_text="Add Label", disabled=False)
        self.submit_button = ft.IconButton(col=4, icon=ft.icons.CHECK, on_click=self.submit_target_card)
        self.choose_dest_button = ft.ElevatedButton("New Destination", col=3,
                                                    icon=ft.icons.FOLDER_OPEN,
                                                    height=ROW_HEIGHT,
                                                    on_click=self.get_target_directory.get_directory_path_async,
                                                    style=ft.ButtonStyle(
                                                        shape=ft.RoundedRectangleBorder(radius=RADIUS)))

        self.target_grid = ft.ResponsiveRow(
            controls=[
                self.create_card(item) for item in self.all_targets["results"]])

        return ft.ResponsiveRow(
            controls=[
                self.section_title,
                self.choose_dest_button,
                self.get_target_directory,
                ft.Column(horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                          col=12,
                          height=MIN_MODULE,
                          scroll=ft.ScrollMode.ALWAYS,
                          controls=[self.target_grid])]
        )
