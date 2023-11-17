import asyncio
import logging
import threading

import flet as ft

from backend.api.main import start_backend
from constants import MAX_MODULE, ROW_HEIGHT, LARGE_SIZE
from frontend.route_controls.format_controls.format_module import FormatControl
from frontend.route_controls.general_controls import CustomElevatedButton, CustomField
from frontend.route_controls.origin_controls.origin_module import OriginControl
from frontend.route_controls.service import Service
from frontend.route_controls.sidebar import SideBar
from frontend.route_controls.target_controls.target_module import TargetControl

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


async def main(page: ft.Page):
    page.window_height = 1000

    async def load(e, message: str = None):
        if message:
            loading_screen.controls.append(ft.Text(message))
        main_layout.controls.remove(main_screen)
        main_layout.controls.append(loading_screen)
        for i in range(0, 101):
            loading_screen.controls[-1].value = i * 0.01
            await asyncio.sleep(0.01)
            await page.update_async()
        await reload_main(e)

    async def reload_main(e):
        main_layout.controls.remove(loading_screen)
        main_layout.controls.append(main_screen)
        await page.update_async()

    async def move(e):
        logger.info("Hello")
        if select_origin.value:
            origin_id = Service.get_origin_by_path(select_origin.value)["id"]
            logger.info(origin_id)
            message = Service.move_files(origin_path=select_origin.value, origin_id=origin_id)
            await load(e, message=str(message))

        pass

    refresh_button = CustomElevatedButton(col=12, icon=ft.icons.REFRESH, text="Refresh", on_click=load)
    move_button = CustomElevatedButton(col=12, icon=ft.icons.PLAY_ARROW, text="Move", on_click=move)
    select_origin = ft.Dropdown(col=12,
                                height=ROW_HEIGHT,
                                hint_text="Choose Origin",
                                text_size=LARGE_SIZE,
                                options=[
                                    ft.dropdown.Option(f"{item['path']}") for item in
                                    Service.get_all_origins()["results"]

                                ])
    loading_screen = ft.Column(col=9,
                               spacing=100,
                               horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                               controls=[
                                   ft.SafeArea(height=MAX_MODULE, content=ft.Text("")),
                                   ft.ProgressRing(width=ROW_HEIGHT, height=ROW_HEIGHT, value=1.0)])
    main_screen = ft.Column(col=9, controls=[OriginControl(), TargetControl(), FormatControl()])
    main_layout = ft.ResponsiveRow(controls=[
        ft.Container(col=3,
                     border=ft.border.only(right=ft.border.BorderSide(1, ft.colors.WHITE)),
                     content=SideBar(col=12,
                                     refresh_button=refresh_button,
                                     move_button=move_button,
                                     origin_dropdown=select_origin)),
        main_screen

    ]
    )

    await page.add_async(
        main_layout

    )


async def start_flet():
    await asyncio.sleep(3)
    await ft.app_async(main)


if __name__ == '__main__':
    uvicorn_thread = threading.Thread(target=start_backend, daemon=True)
    uvicorn_thread.start()
    try:
        asyncio.run(start_flet())
    except KeyboardInterrupt:
        print("Shutting down...")
