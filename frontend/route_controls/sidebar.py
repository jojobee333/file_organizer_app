import flet as ft


class SideBar(ft.UserControl):
    def __init__(self, col):
        super().__init__()
        self.col = col

    def build(self):
        return ft.Container(
            expand=True,
            col=self.col,
            content=ft.Column(controls=[ft.Text("Hello")]

                              ))
