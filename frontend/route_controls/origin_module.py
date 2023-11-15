import asyncio
import json
import logging
import flet as ft
import requests
from flet_core import FilePickerResultEvent
from constants import HEIGHT, url_base, HEADERS, SIZE

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class OriginControl(ft.UserControl):
    # OK
    def __init__(self):
        super().__init__()
        self.origin_text_field = None
        self.origin_data_table = None
        self.delete_button = None
        self.add_origin_button = None
        self.choose_origin_button = None
        self.get_origin_directory = None

    async def add_origin(self, e):
        # OK
        if self.origin_text_field.value:
            url = f"{url_base}/origins/?path={self.origin_text_field.value}"
            response = json.loads(requests.post(headers=HEADERS, url=url).text)
            self.origin_data_table.rows.append(ft.DataRow(
                on_select_changed=self.this_selected,
                selected=False,
                cells=[
                    ft.DataCell(ft.Text(response["id"])),
                    ft.DataCell(ft.Text(response["path"])),
                    ft.DataCell(self.delete_button)
                ]

            ))
            await self.origin_data_table.update_async()
            await self.update_async()

    async def get_directory_result(self, e: FilePickerResultEvent):
        self.origin_text_field.value = e.path if e.path else ""
        await self.update_async()

    async def this_selected(self, e):
        # OK
        e.control.selected = not e.control.selected
        await self.update_async()

    def create_data_row(self, item):

        def delete_button_click(e):
            asyncio.create_task(self.delete_origin(e, item["id"]))

        delete_button = ft.IconButton(
            icon=ft.icons.DELETE,
            on_click=delete_button_click
        )
        return ft.DataRow(
            on_select_changed=self.this_selected,
            selected=False,
            cells=[
                ft.DataCell(ft.Text(item["id"])),
                ft.DataCell(ft.Text(item["path"])),
                ft.DataCell(delete_button)
            ]
        )

    async def delete_origin(self, e, origin_id):
        url = f"{url_base}/origins/{origin_id}"
        response = requests.delete(url=url, headers=HEADERS)
        if response.status_code == 200:
            self.origin_data_table.rows = [
                row for row in self.origin_data_table.rows if row.cells[0].content.value != origin_id
            ]
            await self.origin_data_table.update_async()

    def build(self):
        all_origins = json.loads(requests.get(headers=HEADERS, url=f"{url_base}/origins/").text)
        self.get_origin_directory = ft.FilePicker(on_result=self.get_directory_result)
        self.choose_origin_button = ft.ElevatedButton("Choose New Origin",
                                                      col=3,
                                                      icon=ft.icons.FOLDER_OPEN,
                                                      height=HEIGHT,
                                                      on_click=self.get_origin_directory.get_directory_path_async,
                                                      style=ft.ButtonStyle(
                                                          shape=ft.RoundedRectangleBorder(
                                                              radius=5)))
        self.delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=self.delete_origin)
        self.add_origin_button = ft.IconButton(
            col=1,
            icon=ft.icons.ADD,
            height=HEIGHT,
            on_click=self.add_origin,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            )
        )

        self.origin_text_field = ft.TextField(col=8,
                                              filled=True,
                                              disabled=True,
                                              border_radius=ft.border_radius.all(5),
                                              height=HEIGHT,
                                              text_size=SIZE)
        self.origin_data_table = ft.DataTable(
            show_checkbox_column=True,
            columns=[
                ft.DataColumn(ft.Text("#")),
                ft.DataColumn(ft.Text("Path")),
                ft.DataColumn(ft.Text("Delete"))
            ],
            rows=[
                self.create_data_row(item) for item in all_origins["results"]
            ]
        )
        return ft.ResponsiveRow(
            controls=[
                self.origin_text_field,
                self.add_origin_button,
                self.choose_origin_button,
                self.get_origin_directory,
                ft.Column(horizontal_alignment=ft.CrossAxisAlignment.STRETCH, col=12, height=150,
                          scroll=ft.ScrollMode.ALWAYS, controls=[self.origin_data_table])

            ]
        )
