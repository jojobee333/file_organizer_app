import asyncio
import logging
import threading
import flet as ft
from backend.api.main import start_backend
from constants import MAX_MODULE, ROW_HEIGHT
from frontend.route_controls.format_module import FormatControl
from frontend.route_controls.base_controls import CustomElevatedButton
from frontend.route_controls.origin_module import OriginControl
from frontend.route_controls.sidebar_module import SideBar
from frontend.route_controls.target_module import TargetControl

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class BaseControl(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.main_layout = None
        self.sidebar_container = None
        self.refresh_button = None
        self.main_screen = None
        self.loading_screen = None
        self.select_origin = None
        self.move_button = None

    async def load(self, e, message: str = None):
        if message:
            self.loading_screen.controls.append(ft.Text(message))
        logger.info(self.main_layout.controls)
        self.main_layout.controls.clear()
        self.main_layout.controls.append(self.loading_screen)
        logger.info(self.main_layout.controls)
        for i in range(0, 101):
            self.loading_screen.controls[-1].value = i * 0.01
            await asyncio.sleep(0.001)
            await self.update_async()
        await self.reload_main(e)

    async def reload_main(self, e):
        self.main_layout.controls.clear()
        new_data = self.get_data()
        self.main_screen = ft.Column(col=9, controls=new_data)
        self.main_layout.controls.append(self.sidebar_container)
        self.main_layout.controls.append(self.main_screen)
        await self.page.update_async()
        await self.update_async()

    def get_data(self):
        return [OriginControl(),
                TargetControl(),
                FormatControl()]

    def set_controls(self):

        self.loading_screen = ft.Column(col=12,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                        controls=[
                                            ft.SafeArea(col=12, height=MAX_MODULE, content=ft.Text("")),
                                            ft.ProgressRing(col=12, width=ROW_HEIGHT, height=ROW_HEIGHT, value=1.0)])
        self.main_screen = ft.Column(col=9, controls=self.get_data())
        self.refresh_button = CustomElevatedButton(col=12, icon=ft.icons.REFRESH, text="Refresh", on_click=self.load)
        self.sidebar_container = ft.Container(col=3,
                                              # bgcolor=ft.colors.GREY_900,
                                              shadow=ft.BoxShadow(spread_radius=1.5,
                                                                  offset=ft.Offset(3, 4),
                                                                  color=ft.colors.BLACK12,
                                                                  blur_radius=7),
                                              content=SideBar(col=12, refresh_button=self.refresh_button))
        self.main_layout = ft.ResponsiveRow(
            controls=[
                self.sidebar_container,
                self.main_screen])

    def build(self):
        self.set_controls()
        return self.main_layout


async def main(page: ft.Page):
    page.window_height = 1000

    await page.add_async(
        BaseControl()
    )


async def start_flet():
    await asyncio.sleep(1)
    await ft.app_async(target=main,
                       assets_dir="assets")


if __name__ == '__main__':
    uvicorn_thread = threading.Thread(target=start_backend, daemon=True)
    uvicorn_thread.start()
    try:
        asyncio.run(start_flet())
    except KeyboardInterrupt:
        print("Shutting down...")
