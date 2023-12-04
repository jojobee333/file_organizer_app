import asyncio
import logging
import flet as ft

from constants import MAX_HEIGHT
from frontend.components.components import NavButton
from frontend.main_frame.top_bar import TopBar
from frontend.screens.dashboard_screen import DashboardScreen
from frontend.main_frame.left_bar import LeftBar
from frontend.screens.folder_screen import FolderScreen
from frontend.screens.format_screen import FormatScreen
from frontend.screens.loading_screen import LoadingScreen

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class ScreenManager(ft.UserControl):

    def __init__(self):
        super().__init__()
        self.all_targets = None
        self.all_origins = None
        self.all_formats = None
        self.default_value = None
        self.refresh_button = None
        self.screen_manager_main = None
        self.run_btn = None
        self.schedule_btn = None
        self.format_btn = None
        self.folder_btn = None
        self.dashboard_btn = None
        self.current_screen = None

    async def create_screen(self, screen_type):
        try:
            self.default_value = 10
            if screen_type == "dashboard":
                return DashboardScreen(self.default_value)
            elif screen_type == "folder":
                return FolderScreen(self.default_value)
            elif screen_type == "format":
                return FormatScreen(col=self.default_value)
            elif screen_type == "loading":
                return LoadingScreen()
            else:
                raise ValueError(f"Unknown screen type: {screen_type}.")
        except Exception as e:
            logger.info(e)

    async def switch_screen(self, e, screen_type):
        logger.info(f"Switching to {screen_type} screen.")
        try:
            self.screen_manager_main.controls.remove(self.current_screen)
            self.current_screen = await self.create_screen(screen_type)
            self.screen_manager_main.controls.append(self.current_screen)
            await self.update_async()
            logger.info(f"Switched to {screen_type} screen.")
        except Exception as ex:
            logger.error(f"Error switching screen: {ex}")

    def build(self):
        self.refresh_button = ft.IconButton(col=1, icon=ft.icons.REFRESH,
                                            on_click=lambda e: asyncio.create_task(
                                                self.switch_screen(screen_type="loading", e=e)))
        self.current_screen = DashboardScreen(10)
        # screens
        self.dashboard_btn = NavButton(icon=ft.icons.DASHBOARD,
                                       text="Dashboard",
                                       on_click=lambda e: asyncio.create_task(
                                           self.switch_screen(e, screen_type="dashboard")))
        self.folder_btn = NavButton(icon=ft.icons.FOLDER,
                                    text="Folders",
                                    on_click=lambda e: asyncio.create_task(self.switch_screen(e, screen_type="folder")))

        self.format_btn = NavButton(icon=ft.icons.FORMAT_BOLD, text="Formats",
                                    on_click=lambda e: asyncio.create_task(self.switch_screen(e, screen_type="format")))
        self.schedule_btn = NavButton(icon=ft.icons.TIMER, text="Schedule", on_click=None)
        self.run_btn = NavButton(icon=ft.icons.PLAY_ARROW, text="Run", on_click=None)
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
                        run_btn=self.run_btn
                        ),
                self.current_screen
            ]
        )

        return ft.Column(
            controls=[
                self.screen_manager_main

            ]
        )
