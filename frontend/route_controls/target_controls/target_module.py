import logging
import flet as ft
from flet_core import FilePickerResultEvent

from constants import ROW_HEIGHT, CARD_COLOR, LARGE_SIZE, MAX_MODULE, LARGE_ICON, \
    RADIUS, LARGE_TXT, SMALL_TXT, MIN_MODULE
from frontend.route_controls.general_controls import Title, CustomField
from frontend.route_controls.service import Service
from frontend.route_controls.target_controls.custom_target_card import TargetCard

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class TargetControl(ft.UserControl):
    # OK

    def __init__(self):
        super().__init__()
        self.target_name_field = None
        self.all_targets = None
        self.target_folder_icon = None
        self.target_grid = None
        self.get_target_directory = None
        self.section_title = None
        self.choose_dest_button = None
        self.submit_button = None

    async def get_directory_result(self, e: FilePickerResultEvent):
        target_path = e.path if e.path else ""
        if target_path:
            self.new_destination_card(target_path)
        await self.update_async()

    def new_destination_card(self, target_path):
        self.target_grid.controls.append(
            TargetCard(
                color=CARD_COLOR,
                items=[
                    self.target_folder_icon,
                    ft.ResponsiveRow(controls=[self.target_name_field, self.submit_button]),
                    ft.Text(target_path, size=SMALL_TXT, no_wrap=True, max_lines=1)]))

    async def submit_target_card(self, e):
        """Submit the target card and add target to database."""
        label = self.target_name_field.value
        items = self.target_grid.controls[-1].items
        path = items[-1].value
        items.remove(self.target_grid.controls[-1].items[1])
        items.insert(1, ft.Text(label, size=LARGE_SIZE, weight=ft.FontWeight.BOLD))
        Service.add_target(target_label=label, target_path=path)
        await self.update_async()

    def populate_grid(self, item):
        return TargetCard(
            color=CARD_COLOR,
            items=[
                self.target_folder_icon,
                ft.Text(item["name"], size=LARGE_TXT, weight=ft.FontWeight.BOLD),
                ft.Text(item["path"], size=SMALL_TXT, no_wrap=True, max_lines=1, overflow=ft.TextOverflow.FADE)
            ])

    def build(self):
        all_targets = Service.get_all_targets()
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
        self.target_folder_icon = ft.Icon(ft.icons.FOLDER, size=LARGE_ICON)
        self.target_grid = ft.ResponsiveRow(
            controls=[
                self.populate_grid(item) for item in all_targets["results"]])

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
