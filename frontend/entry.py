import asyncio
import logging
import threading

import flet as ft
import uvicorn

from backend.api.main import app
from constants import HOST, PORT
from frontend.route_controls.format_module import FormatControl
from frontend.route_controls.origin_module import OriginControl
from frontend.route_controls.target_module import TargetControl

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


async def main(page: ft.Page):
    # hide all dialogs in overlay
    await page.add_async(
        ft.ResponsiveRow(

            controls=[OriginControl(),
                      TargetControl(),
                      # FormatControl()
            ]
        ),

    )


async def start_flet():
    await ft.app_async(main)


def start_backend():
    uvicorn.run("backend.api.main:app", host=HOST, port=PORT, reload=False)


if __name__ == '__main__':
    uvicorn_thread = threading.Thread(target=start_backend, daemon=True)
    uvicorn_thread.start()
    try:
        # Start the Flet app with delay
        asyncio.run(start_flet())
    except KeyboardInterrupt:
        print("Shutting down gracefully")


