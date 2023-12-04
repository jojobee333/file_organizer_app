import asyncio
import flet as ft


class LoadingScreen(ft.UserControl):

    def __init__(self):
        super().__init__()
        self.size = 40
        self.countdown = None
        self.running = None

    def build(self):
        return ft.Column(col=12, controls=[

            ft.ProgressRing(
                width=self.size,
                height=self.size),
            self.countdown
        ])
