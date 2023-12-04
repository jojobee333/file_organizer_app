import logging
import flet as ft
from frontend.components.components import ScreenContainer, DashboardContainer, BulletedItem, \
    Title, SingleItemLogRow, ListScroller

from frontend.controllers.screen_controller import ScreenController

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class DashboardScreen(ft.UserControl):

    def __init__(self, col, screen_controller: ScreenController):
        super().__init__()
        self.scheduled_items = None
        self.recent_items = None
        self.today_items = None
        self.format_container = None
        self.target_container = None
        self.origin_container = None
        self.format_content = None
        self.target_content = None
        self.origin_content = None
        self.all_origins = None
        self.all_formats = None
        self.all_targets = None
        self.main_column = None
        self.today_title = None
        self.scheduled_title = None
        self.recent_title = None
        self.activity_title = None
        self.title_divider = None
        self.dashboard_title = None
        self.screen_type = None
        self.controller = screen_controller
        self.col = col



    def initialize_attributes(self):
        self.screen_type = "dashboard"
        self.dashboard_title = Title("Dashboard")
        self.title_divider = ft.Divider(thickness=0.0, height=1, color=ft.colors.WHITE)
        self.activity_title = Title("Activity")
        self.recent_title = ft.Text("Recent")
        self.today_title = ft.Text("Today")
        self.scheduled_title = ft.Text("Scheduled Runs")
        self.main_column = None

    def get_data(self):
        try:
            self.all_targets = self.controller.get_targets()["results"]
            self.all_formats = self.controller.get_formats()["results"]
            self.all_origins = self.controller.get_origins()["results"]
        except Exception as e:
            logger.error(e)

    @staticmethod
    def create_dashboard_container(title, amount, unit, icon_type, content):
        return DashboardContainer(title=title, amount=amount, unit=unit,
                                  icon_type=icon_type, on_click=None, content=content)

    @staticmethod
    def create_content_list(items, icon_color=ft.colors.CYAN):
        return [BulletedItem(icon_color=icon_color, item_name=item["name"]) for item in items] if items else [
            ft.Text("None")]

    @staticmethod
    def create_list_scroller(name, count, date):
        return ListScroller(
            horizontal=True,
            controls=[SingleItemLogRow(name=name, files_moved=num, date=date) for num in range(count)]
        )

    def get_components(self):
        self.origin_content = DashboardScreen.create_content_list(self.all_origins)
        self.target_content = DashboardScreen.create_content_list(self.all_targets)
        self.format_content = DashboardScreen.create_content_list(self.all_formats)

        self.origin_container = DashboardScreen.create_dashboard_container("Origins", len(self.all_origins),
                                                                           "Folders", ft.icons.FOLDER,
                                                                           self.origin_content)
        self.target_container = DashboardScreen.create_dashboard_container("Destinations", len(self.all_targets),
                                                                           "Folders", ft.icons.FOLDER,
                                                                           self.target_content)
        self.format_container = DashboardScreen.create_dashboard_container("Formats", len(self.all_formats),
                                                                           "Mapped Formats", ft.icons.TYPE_SPECIMEN,
                                                                           self.format_content)

        self.today_items = DashboardScreen.create_list_scroller("My Documents", 3, "11/26/23")
        self.recent_items = DashboardScreen.create_list_scroller("My Downloads", 5, "11/26/23")
        self.scheduled_items = DashboardScreen.create_list_scroller("My Downloads", 7, "11/26/23")

        self.main_column = ft.SafeArea(
            minimum=10,
            content=ft.Column(
                scroll=ft.ScrollMode.ALWAYS,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                col=12,
                controls=[
                    self.dashboard_title, self.title_divider,
                    self.origin_container, self.target_container, self.format_container,
                    self.activity_title, self.today_title, self.today_items,
                    self.recent_title, self.recent_items, self.scheduled_title, self.scheduled_items
                ]))

    def build(self):
        self.get_data()
        self.initialize_attributes()
        self.get_components()
        return ScreenContainer(
            content=self.main_column)
