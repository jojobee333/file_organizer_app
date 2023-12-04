import asyncio
import logging
import flet as ft
from backend.service import Service
from constants import MAX_HEIGHT
from frontend.components.components import ScreenContainer, Title, ListScroller, SingleItemFileRow, AlertBox, \
    AlertField, Selector, Tag, OKButton, AddButton, SingleItemFormatRow
from frontend.control_handlers.alert_handler import AlertHandler

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class FormatScreen(ft.UserControl):
    def __init__(self, col):
        super().__init__()
        self.col = col
        self.screen_type = "format"
        self.format_title = Title("Formats", col=10)
        self.title_divider = ft.Divider(thickness=0.0, height=1, color=ft.colors.WHITE)
        self.all_formats = Service().get_all_formats()["results"]
        self.all_targets = Service().get_all_targets()["results"]
        self.screen_container = None
        self.alert = None
        self.add_format_btn = AddButton(on_click=self.add_format_alert)
        self.formats_dropdown = None
        self.format_items = None
        self.main_column = ft.Column(alignment=ft.MainAxisAlignment.START, col=12, controls=[])

    def reload_data(self):
        # may be throwing an error
        # throws errors when a format that is invalid is in the database.
        try:
            format_response = Service().get_all_formats()
            self.all_formats = format_response["results"]
            target_response = Service().get_all_targets()
            self.all_targets = target_response["results"]

        except Exception as e:
            logger.error(e)

    def make_format_section(self):
        self.format_items = ListScroller(
            height=MAX_HEIGHT,
            controls=[
                self.populate_formats(
                    format_name=fmt["name"],
                    target=Service.get_target_by_id((fmt["target_id"]))["name"])
                for fmt in self.all_formats])

    async def reload_page(self):
        # needs work
        progress_ring = ft.ProgressBar(width=50)
        self.main_column.controls.clear()
        self.main_column.controls.append(ft.ResponsiveRow(
            expand=True,
            col=12,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[progress_ring]))
        await self.update_async()

    async def delete_format(self, e, format_name):
        try:
            response = Service.get_format_by_name(format_name)
            if response["id"]:
                format_id = response["id"]
                Service.delete_format(format_id)
                self.format_items.controls = [row for row in self.format_items.controls if row.content.controls[1].value != format_name]
                await self.update_async()
        except Exception as e:
            logger.error(e)

    def populate_targets(self, target_name, target_id):
        return ft.dropdown.Option(text=target_name, key=target_id)

    def populate_formats(self, format_name, target):
        return SingleItemFormatRow(name=format_name,
                                   location=target,
                                   on_click=lambda e: asyncio.create_task(self.delete_format(format_name=format_name, e=e)))

    async def add_format(self, format_name, target_id, e):
        if format_name and target_id:
            logger.info(f"format_name : {format_name}, target_id = {target_id}")
            Service.add_format(format_name=format_name, target_id=target_id)
            await AlertHandler.close_alert(e=e, page=self.page, alert=self.alert)

    async def add_format_alert(self, e):
        name_field = AlertField(label="format name", hint_text="example : exe", col=12, disabled=False)
        target_options = [self.populate_targets(target["name"], target_id=target["id"]) for target in self.all_targets]
        target_dropdown = Selector(col=12, options=target_options, hint_text="Choose Target")
        ok_button = OKButton(on_click=lambda e: asyncio.create_task(self.add_format(format_name=name_field.value,
                                                                                    target_id=target_dropdown.value,
                                                                                    e=e)))

        self.alert = AlertBox(title=Title("New Format"), actions=[
            name_field,
            target_dropdown,
            ok_button

        ], tag=Tag.NEW_FORMAT)
        await AlertHandler.open_alert(page=self.page, alert=self.alert)

    def build_main_column(self):

        self.main_column.controls = [
            ft.ResponsiveRow(col=12,
                             controls=[self.format_title, self.add_format_btn]),
            self.title_divider,
            self.format_items]

    def build(self):
        self.make_format_section()
        self.build_main_column()

        return ScreenContainer(content=ft.SafeArea(
            minimum=10,
            content=self.main_column))
