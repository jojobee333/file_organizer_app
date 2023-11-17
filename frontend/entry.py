import asyncio
import logging
import threading

import flet as ft

from backend.api.main import start_backend
from frontend.route_controls.format_controls.format_module import FormatControl
from frontend.route_controls.origin_controls.origin_module import OriginControl
from frontend.route_controls.sidebar import SideBar
from frontend.route_controls.target_controls.target_module import TargetControl

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


async def main(page: ft.Page):
    page.window_height = 1000
    # hide all dialogs in overlay
    await page.add_async(
        ft.ResponsiveRow(
            controls=[ft.Container(col=2,
                                   border=ft.border.only(right=ft.border.BorderSide(1, ft.colors.WHITE)),
                                   content=SideBar(col=12)),
                      ft.Column(col=10, controls=[OriginControl(),
                                                  TargetControl(),
                                                  FormatControl()
                                                  ])
                      ]
        ),

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
