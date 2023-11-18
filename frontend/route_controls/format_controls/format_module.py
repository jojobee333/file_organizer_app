import asyncio
import logging
import flet as ft
from constants import ROW_HEIGHT, MAX_MODULE, LARGE_SIZE
from frontend.route_controls.alert_handler import AlertHandler
from frontend.route_controls.exception_controls.custom_exceptions import InvalidEntryException
from frontend.route_controls.base_controls import Title, CustomElevatedButton, CustomField
from frontend.route_controls.service import Service

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class FormatControl(ft.UserControl):
    def __init__(self, all_formats, all_targets):
        super().__init__()
        self.all_formats = all_formats
        self.all_targets = all_targets
        self.section_title = None
        self.alert_handler = None
        self.format_data_table = None
        self.format_name_field = None
        self.new_format_button = None
        self.target_dropdown = None

    def create_data_row(self, item):
        try:
            def delete_button_click(e):
                asyncio.create_task(self.delete_format_card(e, item["id"]))

            delete_button = ft.IconButton(col=2,
                                          icon=ft.icons.DELETE,
                                          on_click=delete_button_click
                                          )

            target = Service.get_target_by_id(item["target_id"])
            target_name = target["name"] if target else ""
            return ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(item["id"], col=2)),
                    ft.DataCell(ft.Text(item["name"], col=3, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(ft.Text(target_name, col=4)),
                    ft.DataCell(delete_button)

                ]
            )
        except Exception as e:
            logger.info(e)

    async def delete_format_card(self, e, format_id):
        """Deletes format from database and deletes the row."""
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

    @staticmethod
    def validate_format_name(format_name):
        """Validates the format name."""
        if format_name[0] != ".":
            return False
        if len(format_name) < 2:
            return False
        return True

    async def submit_format_row(self, e):
        """Submits the format to database, finalizes the row"""
        # working
        try:
            if not self.format_name_field or not self.target_dropdown.value:
                raise InvalidEntryException("Format is Invalid.")

            if self.format_name_field.value and self.target_dropdown.value:
                if not FormatControl.validate_format_name(self.format_name_field.value):

                    format_name = self.format_name_field.value
                    target_id = Service.get_target_by_name(self.target_dropdown.value)["id"]
                    response = Service.add_format(format_name=format_name, target_id=int(target_id))

                    if response["code"] == 200:
                        new_format = Service.get_format_by_name(format_name)
                        for row in self.format_data_table.rows:
                            logger.info(row.cells[1].content.value)
                            if row.cells[1].content.value == format_name:
                                self.format_data_table.rows.remove(row)
                                self.format_data_table.rows.append(self.create_data_row(item=new_format))
                                await self.update_async()
        except InvalidEntryException as err:
            logger.info(err)

            async def close_button_click(e):
                asyncio.create_task(AlertHandler.close_alert(e, alert=alert, page=self.page))

            alert = ft.AlertDialog(title=ft.Text("Invalid Name"),
                                   content=ft.Text("The format name you entered is invalid."),
                                   actions=[ft.TextButton("OK", on_click=close_button_click)])
            await AlertHandler.open_alert(alert=alert, page=self.page)

        except Exception as e:
            logger.info(e)

    async def format_row_draft(self, e):
        """Create new format in format data table."""
        try:
            def submit_button_click(e):
                """Event handler for newly created submit buttons in the format rows."""
                asyncio.create_task(self.submit_format_row(e))

            submit_button = ft.IconButton(icon=ft.icons.CHECK, col=2, on_click=submit_button_click)
            self.target_dropdown = ft.Dropdown(col=4,
                                               height=ROW_HEIGHT,
                                               hint_text="Choose Target",
                                               text_size=LARGE_SIZE,
                                               autofocus=True,
                                               options=[
                                                   ft.dropdown.Option(f"{item['name']}") for item in
                                                   self.all_targets["results"]

                                               ])
            self.format_data_table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text("-")),
                    ft.DataCell(self.format_name_field),
                    ft.DataCell(self.target_dropdown),
                    ft.DataCell(submit_button)

                ])
            )
            await self.update_async()
        except Exception as e:
            logger.info(e)

    def build(self):
        self.section_title = Title("Formats", col=9)
        self.format_name_field = CustomField(col=3, hint_text=".exe", disabled=False)
        self.format_data_table = ft.DataTable(col=12,
                                              columns=[
                                                  ft.DataColumn(ft.Text("id", col=2)),
                                                  ft.DataColumn(ft.Text("Name", col=6)),
                                                  ft.DataColumn(ft.Text("Destination", col=6)),
                                                  ft.DataColumn(ft.Text("Delete"))],
                                              rows=[self.create_data_row(item=item) for item in
                                                    self.all_formats["results"]])
        self.new_format_button = CustomElevatedButton(text="New Format", col=3, on_click=self.format_row_draft,
                                                      icon=ft.icons.FOLDER_OPEN)
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
