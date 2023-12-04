import asyncio
import logging
import flet as ft
from backend.service import Service
from constants import ROW_HEIGHT, MAX_HEIGHT
from frontend.components.components import ScreenContainer, DashboardContainer, BulletedItem, \
    Title, SingleItemLogRow, ListScroller, SingleItemFileRow, AlertBox, AlertField, Selector, Tag, OKButton
from frontend.screens.alert_handler import AlertHandler

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class FormatScreen(ft.UserControl):
    def __init__(self, col):
        super().__init__()
        self.screen_type = "format"
        self.title_divider = None
        self.all_formats = None
        self.all_targets = None
        self.main_column = None
        self.alert = None
        self.add_format_btn = None
        self.col = col
        self.formats_dropdown = None
        self.format_title = None
        self.format_items = None

    def get_data(self):
        # may be throwing an error
        # throws errors when a format that is invalid is in the database.
        try:
            format_response = Service().get_all_formats()
            self.all_formats = format_response["results"]
            target_response = Service().get_all_targets()
            self.all_targets = target_response["results"]

            logger.info(self.all_targets)
            if isinstance(self.all_formats, list):
                format_controls = [
                    self.populate_formats(
                        format_name=fmt["name"],
                        target=Service.get_target_by_id((fmt["target_id"]))["name"])
                    for fmt in self.all_formats]
            else:
                format_controls = [ft.Text("None")]

            self.format_items = ListScroller(
                height=MAX_HEIGHT,
                controls=format_controls)
            logging.info("Format Section created")
        except Exception as e:
            logger.error(e)

    def populate_targets(self, target_name, target_id):
        return ft.dropdown.Option(text=target_name, key=target_id)

    def populate_formats(self, format_name, target):
        return SingleItemFileRow(name=format_name, location=target)

    async def add_format(self, format_name, target_id, e):
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

    def get_components(self):
        self.get_data()
        self.format_title = Title("Formats", col=5)
        self.add_format_btn = ft.IconButton(col=1, icon=ft.icons.ADD, icon_size=20, height=ROW_HEIGHT,
                                            on_click=self.add_format_alert,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)))

        self.title_divider = ft.Divider(thickness=0.0, height=1, color=ft.colors.WHITE)

        self.main_column = ft.SafeArea(
            minimum=10,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                col=12,
                controls=[
                    ft.ResponsiveRow(col=12,
                                     controls=[
                                         self.format_title,
                                         self.add_format_btn
                                     ],
                                     alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    self.title_divider,
                    self.format_items

                ]))

    def build(self):
        self.get_components()

        return ScreenContainer(
            content=self.main_column
        )
