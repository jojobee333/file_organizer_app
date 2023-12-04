import asyncio
import threading

import flet as ft

from backend.api_init import start_backend
from constants import MAX_HEIGHT
from frontend.screens.screenmanager import ScreenManager


async def main(page: ft.Page):
    page.title = "File Manager"
    page.window_height = MAX_HEIGHT
    page.padding = 0
    page.bgcolor = ft.colors.with_opacity(1.0, '#3A3A3A')

    page.dark_theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=ft.colors.with_opacity(1.0, '#3A3A3A'),
            primary_container=ft.colors.with_opacity(1.0, '#3A3A3A')),
        font_family="Gadugi",
        use_material3=True
    )

    await page.add_async(
        ScreenManager()
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
