import logging
import flet as ft
from backend.service import Service
from frontend.components.components import ScreenContainer, DashboardContainer, BulletedItem, \
    Title, SingleItemLogRow, ListScroller

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class DashboardScreen(ft.UserControl):
    def __init__(self, col):
        super().__init__()
        self.screen_type = "dashboard"
        self.col = col
        self.all_targets = None
        self.all_formats = None
        self.all_origins = None
        self.dashboard_title = None

    def get_data(self):
        self.all_targets = Service().get_all_targets()["results"]
        self.all_formats = Service().get_all_formats()["results"]
        self.all_origins = Service().get_all_origins()["results"]

    def build(self):
        self.get_data()
        origin_content = [BulletedItem(icon_color=ft.colors.CYAN, item_name=origin["name"]) for origin in
                          self.all_origins] if self.all_origins else [ft.Text("None")]
        target_content = [BulletedItem(icon_color=ft.colors.CYAN, item_name=target["name"]) for target in
                          self.all_targets] if self.all_targets else [ft.Text("None")]
        format_content = [BulletedItem(icon_color=ft.colors.CYAN, item_name=format["name"]) for format in
                          self.all_formats] if self.all_formats else [ft.Text("None")]
        self.dashboard_title = Title("Dashboard")
        activity_title = Title("Activity")
        recent_title = ft.Text("Recent")
        today_title = ft.Text("Today")
        scheduled_title = ft.Text("Scheduled Runs")

        title_divider = ft.Divider(thickness=0.0, height=1, color=ft.colors.WHITE)
        origin_container = DashboardContainer(title="Origins", amount=len(self.all_origins), unit="Folders",
                                              icon_type=ft.icons.FOLDER,
                                              on_click=None,
                                              content=origin_content)
        target_container = DashboardContainer(title="Destinations", amount=len(self.all_targets), unit="Folders",
                                              icon_type=ft.icons.FOLDER,
                                              on_click=None,
                                              content=target_content)
        format_container = DashboardContainer(title="Formats", amount=len(self.all_formats),
                                              unit="Mapped Formats",
                                              icon_type=ft.icons.TYPE_SPECIMEN,
                                              on_click=None,
                                              content=format_content)
        today_items = ListScroller(
            horizontal=True,
            controls=[SingleItemLogRow(name="My Documents", files_moved=num, date="11/26/23") for num in range(3)]
        )
        recent_items = ListScroller(
            horizontal=True,
            controls=[SingleItemLogRow(name="My Downloads", files_moved=num, date="11/26/23") for num in range(5)]
        )
        scheduled_items = ListScroller(
            horizontal=True,
            controls=[SingleItemLogRow(name="My Downloads", files_moved=num, date="11/26/23") for num in range(7)]
        )

        main_column = (
            ft.SafeArea(
                minimum=10,
                content=ft.Column(
                    scroll=ft.ScrollMode.ALWAYS,
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                    col=12,
                    controls=[
                        self.dashboard_title,
                        title_divider,
                        # containers
                        origin_container,
                        target_container,
                        format_container,
                        # activity
                        activity_title,
                        today_title,
                        today_items,
                        recent_title,
                        recent_items,
                        # scheduled
                        scheduled_title,
                        scheduled_items

                    ])))

        return ScreenContainer(
            content=main_column
        )
