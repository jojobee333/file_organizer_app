import asyncio
import json
import logging
import flet as ft
import requests

from constants import url_base, HEADERS, ROW_HEIGHT, MAX_MODULE, LARGE_SIZE
from frontend.route_controls.format_controls.custom_format_card import FormatCard
from frontend.route_controls.general_controls import Title, CustomElevatedButton, CustomField
from frontend.route_controls.service import Service

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class FormatControl(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.section_title = None
        self.all_formats = None
        self.format_list = None
        self.format_name_field = None
        self.new_format_button = None
        self.target_dropdown = None
        self.all_targets = None

    def populate_format_list(self, item):
        def delete_button_click(e):
            asyncio.create_task(self.delete_format(e, item["id"]))

        delete_button = ft.IconButton(col=2,
                                      icon=ft.icons.DELETE,
                                      on_click=delete_button_click
                                      )
        return FormatCard(
            items=[
                ft.Text(item["id"], col=2),
                ft.Text(item["name"], col=3, weight=ft.FontWeight.BOLD),
                ft.Text(Service.get_target_by_id(item['target_id'])["name"], col=4),
                delete_button

            ]
        )

    async def delete_format(self, e, format_id):
        # OK
        response = Service.delete_format(format_id)
        if response.status_code == 200:
            for item in self.format_list.controls:
                # logger.info(type(item.items[0].value))
                if item.items[0].value == format_id:
                    self.format_list.controls.remove(item)
                    await self.format_list.update_async()

    async def submit_format_card(self, e):
        # working
        format_name = self.format_name_field.value
        target_id = Service.get_target_by_name(self.target_dropdown.value)["id"]
        response = Service.add_format(format_name=format_name, target_id=int(target_id))
        if response["code"] == 200:
            new_format = Service.get_format_by_name(format_name)
            for item in self.format_list.controls:
                first_value = item.items[0].value
                if isinstance(first_value, str):
                    self.format_list.controls.remove(item)
                    self.format_list.controls.append(self.populate_format_list(new_format))
                    await self.format_list.update_async()

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
        self.format_list.controls.append(
            FormatCard(items=[
                self.format_name_field,
                self.target_dropdown,
                submit_button

            ])
        )
        await self.format_list.update_async()

    def build(self):
        self.all_formats = Service.get_all_formats()
        self.section_title = Title("Formats", col=9)
        self.format_name_field = ft.TextField(col=3, hint_text=".exe", disabled=False,
                                              border_radius=ft.border_radius.all(5),
                                              height=ROW_HEIGHT, text_size=LARGE_SIZE)

        self.format_list = ft.ResponsiveRow(

            controls=[self.populate_format_list(item=item) for item in self.all_formats["results"]])

        self.new_format_button = CustomElevatedButton(text="New Format", col=3, on_click=self.new_format_card)
        return ft.Column(
            scroll=ft.ScrollMode.ADAPTIVE,
            height=MAX_MODULE,
            col=12,
            controls=[
                ft.ResponsiveRow(col=12, controls=[self.section_title, self.new_format_button]),
                self.format_list
            ]
        )
