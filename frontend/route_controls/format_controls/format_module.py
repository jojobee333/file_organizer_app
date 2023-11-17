import asyncio
import logging
import flet as ft

from backend.schemas import Format
from constants import ROW_HEIGHT, MAX_MODULE, LARGE_SIZE
from frontend.route_controls.general_controls import Title, CustomElevatedButton
from frontend.route_controls.service import Service

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class FormatControl(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.section_title = None
        self.all_formats = None
        self.format_data_table = None
        self.format_name_field = None
        self.new_format_button = None
        self.target_dropdown = None
        self.all_targets = None

    def create_data_row(self, item):
        logger.info(item)

        def delete_button_click(e):
            asyncio.create_task(self.delete_format(e, item["id"]))

        delete_button = ft.IconButton(col=2,
                                      icon=ft.icons.DELETE,
                                      on_click=delete_button_click
                                      )

        target = Service.get_target_by_id(item["target_id"])
        # if target id exists, then associate target name with third data cell, else leave empty
        if target:
            target_name = target["name"]
        else:
            target_name = ""
        return ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(item["id"], col=2)),
                ft.DataCell(ft.Text(item["name"], col=3, weight=ft.FontWeight.BOLD)),
                ft.DataCell(ft.Text(target_name, col=4)),
                ft.DataCell(delete_button)

            ]
        )

    async def delete_format(self, e, format_id):
        # OK
        try:
            response = Service.delete_format(format_id)
            if response.status_code == 200:
                for row in self.format_data_table.rows:
                    if row.cells[0].content.value == format_id:
                        self.format_data_table.rows = [
                            row for row in self.format_data_table.rows if row.cells[0].content.value != format_id
                        ]
                        await self.update_async()
            else:
                logger.info("False")
        except Exception as e:
            logger.error(e)

    async def submit_format_card(self, e):
        # working
        format_name = self.format_name_field.value
        target_id = Service.get_target_by_name(self.target_dropdown.value)["id"]
        response = Service.add_format(format_name=format_name, target_id=int(target_id))
        if response["code"] == 200:
            new_format = Service.get_format_by_name(format_name)
            for row in self.format_data_table.rows:
                logger.info(row.cells[1].content.value)
                if row.cells[1].content.value == format_name:
                    logger.info("true")
                    self.format_data_table.rows.remove(row)
                    self.format_data_table.rows.append(self.create_data_row(item=new_format))
                    await self.update_async()

    async def new_format_card(self, e):
        # working
        def submit_button_click(e):
            asyncio.create_task(self.submit_format_card(e))

        submit_button = ft.IconButton(icon=ft.icons.CHECK, col=2, on_click=submit_button_click)
        self.target_dropdown = ft.Dropdown(col=4,
                                           height=ROW_HEIGHT,
                                           hint_text="Choose Target",
                                           text_size=LARGE_SIZE,
                                           autofocus=True,
                                           options=[
                                               ft.dropdown.Option(f"{item['name']}") for item in
                                               Service.get_all_targets()["results"]

                                           ])
        self.format_data_table.rows.append(
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("-")),
                ft.DataCell(self.format_name_field),
                ft.DataCell(self.target_dropdown),
                ft.DataCell(submit_button)

            ])
        )
        await self.format_data_table.update_async()

    def build(self):
        self.all_formats = Service.get_all_formats()
        self.section_title = Title("Formats", col=9)
        self.format_name_field = ft.TextField(col=3, hint_text=".exe", disabled=False,
                                              border_radius=ft.border_radius.all(5),
                                              height=ROW_HEIGHT, text_size=LARGE_SIZE)
        self.format_data_table = ft.DataTable(
            col=12,
            columns=[
                ft.DataColumn(ft.Text("id", col=2)),
                ft.DataColumn(ft.Text("Name", col=6)),
                ft.DataColumn(ft.Text("Destination", col=6)),
                ft.DataColumn(ft.Text("Delete"))],

            rows=[self.create_data_row(item=item) for item in self.all_formats["results"]])
        self.new_format_button = CustomElevatedButton(text="New Format", col=3, on_click=self.new_format_card, icon=ft.icons.FOLDER_OPEN)
        return ft.Column(
            scroll=ft.ScrollMode.ADAPTIVE,
            height=MAX_MODULE,
            col=12,
            controls=[
                ft.ResponsiveRow(col=12, controls=[self.section_title,
                                                   self.new_format_button,
                                                   self.format_data_table]),

            ]
        )
