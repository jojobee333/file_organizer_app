import asyncio
import logging
import flet as ft
from flet_core import FilePickerResultEvent

from constants import MIN_MODULE
from frontend.route_controls.base_controls import AddButton, CustomField, CustomElevatedButton
from frontend.service.service import Service

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class OriginControl(ft.UserControl):
    # OK
    def __init__(self):
        super().__init__()
        self.origin_text_field = None
        self.origin_data_table = None
        self.add_origin_button = None
        self.choose_origin_button = None
        self.get_origin_directory = None
        self.all_origins = Service.get_all_origins()

    async def add_origin(self, e):
        # OK
        if self.origin_text_field.value:
            response = Service.add_origin(self.origin_text_field.value)

            def delete_button_click(e):
                asyncio.create_task(self.delete_origin(e, response["id"]))

            delete_button = ft.IconButton(
                icon=ft.icons.DELETE,
                on_click=delete_button_click
            )

            self.origin_data_table.rows.append(ft.DataRow(
                on_select_changed=self.this_selected,
                selected=False,
                cells=[
                    ft.DataCell(ft.Text(response["id"])),
                    ft.DataCell(ft.Text(response["path"])),
                    ft.DataCell(delete_button)
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
        try:
            response = Service.delete_origin(origin_id)
            if response.status_code == 200:
                self.origin_data_table.rows = [
                    row for row in self.origin_data_table.rows if row.cells[0].content.value != origin_id
                ]
                await self.origin_data_table.update_async()
        except Exception as e:
            logger.error(e)

    def build(self):
        self.get_origin_directory = ft.FilePicker(on_result=self.get_directory_result)
        self.choose_origin_button = CustomElevatedButton(text="Choose New Origin",
                                                         col=3,
                                                         on_click=self.get_origin_directory.get_directory_path_async,
                                                         icon=ft.icons.FOLDER_OPEN)
        self.add_origin_button = AddButton(col=1, on_click=self.add_origin)
        self.origin_text_field = CustomField(col=8, disabled=True, hint_text="New Origin Path")
        self.origin_data_table = ft.DataTable(col=12,
                                              show_checkbox_column=True,
                                              columns=[
                                                  ft.DataColumn(ft.Text("id", col=2)),
                                                  ft.DataColumn(ft.Text("Path", col=6)),
                                                  ft.DataColumn(ft.Text("Delete", col=3))
                                              ],
                                              rows=[
                                                  self.create_data_row(item) for item in self.all_origins["results"]
                                              ]
                                              )
        return ft.ResponsiveRow(
            controls=[
                self.origin_text_field,
                self.add_origin_button,
                self.choose_origin_button,
                self.get_origin_directory,
                ft.Column(horizontal_alignment=ft.CrossAxisAlignment.STRETCH, col=12, height=MIN_MODULE,
                          scroll=ft.ScrollMode.ALWAYS, controls=[self.origin_data_table])

            ]
        )
