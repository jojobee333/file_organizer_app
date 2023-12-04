import asyncio
import logging
import flet as ft

from backend.service import Service
from constants import MAX_HEIGHT
from frontend.components.components import NavButton
from frontend.controllers.screen_controller import ScreenController
from frontend.main_frame.top_bar import TopBar
from frontend.screens.dashboard_screen import DashboardScreen
from frontend.main_frame.left_bar import LeftBar
from frontend.screens.folder_screen import FolderScreen
from frontend.screens.format_screen import FormatScreen
from frontend.screens.loading_screen import LoadingScreen
from frontend.screens.run_screen import RunScreen

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class ScreenManager(ft.UserControl):

    def __init__(self):
        super().__init__()
        self.run_btn = None
        self.schedule_btn = None
        self.format_btn = None
        self.dashboard_btn = None
        self.folder_btn = None
        self.refresh_btn = None
        self.service = Service()
        self.screen_controller = ScreenController(self.service)
        self.default_value = 10
        self.screen_manager_main = None
        self.current_screen = None
        self.screen_classes = {
            "dashboard": DashboardScreen,
            "folder": FolderScreen,
            "format": FormatScreen,
            "run": RunScreen,
            "loading": LoadingScreen
        }
        self.initialize_buttons()

    def initialize_buttons(self):
        self.refresh_btn = self.create_nav_button(ft.icons.REFRESH, "Refresh", "loading")
        self.dashboard_btn = self.create_nav_button(ft.icons.DASHBOARD, "Dashboard", "dashboard")
        self.folder_btn = self.create_nav_button(ft.icons.FOLDER, "Folders", "folder")
        self.format_btn = self.create_nav_button(ft.icons.FORMAT_BOLD, "Formats", "format")
        self.schedule_btn = NavButton(icon=ft.icons.TIMER, text="Schedule", on_click=None)
        self.run_btn = self.create_nav_button(ft.icons.PLAY_ARROW, "Run", "run")

    def create_nav_button(self, icon, text, screen_type):
        return NavButton(icon=icon, text=text, on_click=lambda e: asyncio.create_task(
            self.switch_screen(e, screen_type)))

    def create_screen(self, screen_type):
        try:
            screen_class = self.screen_classes.get(screen_type)
            if screen_class:
                return screen_class(col=self.default_value, screen_controller=self.screen_controller)
            else:
                raise ValueError(f"Unknown screen type: {screen_type}.")
        except Exception as e:
            logger.error(f"Error creating screen {screen_type}: {e}")

    async def switch_screen(self, e, screen_type):
        logger.info(f"Switching to {screen_type} screen.")
        try:
            self.screen_manager_main.controls.remove(self.current_screen)
            self.current_screen = self.create_screen(screen_type)
            self.screen_manager_main.controls.append(self.current_screen)
            await self.update_async()
            logger.info(f"Switched to {screen_type} screen.")
        except Exception as ex:
            logger.error(f"Error switching screen: {ex}")

    def build(self):
        self.current_screen = self.create_screen("dashboard")
        self.screen_manager_main = ft.ResponsiveRow(
            height=MAX_HEIGHT,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[
                TopBar(col=12),
                LeftBar(col=2,
                        dashboard_btn=self.dashboard_btn,
                        folder_btn=self.folder_btn,
                        format_btn=self.format_btn,
                        schedule_btn=self.schedule_btn,
                        run_btn=self.run_btn),
                self.current_screen
            ]
        )
        return ft.Column(controls=[self.screen_manager_main])
