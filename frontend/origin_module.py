import json
import logging
import flet as ft
import requests
from flet_core import FilePickerResultEvent
from constants import HEIGHT, url_base, HEADERS, SIZE

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class OriginControl(ft.UserControl):
    def __init__(self):

        super().__init__()

    def build(self):
        def get_directory_result(e: FilePickerResultEvent):
            origin_text_field.value = e.path if e.path else ""
            self.update()

        def this_selected(e):
            e.control.selected = not e.control.selected
            self.update()

        def add_origin():
            if origin_text_field.value:
                url = f"{url_base}/origins/?path={origin_text_field.value}"
                response = json.loads(requests.post(headers=HEADERS, url=url).text)
                origin_data_table.rows.append(ft.DataRow(
                    on_select_changed=this_selected,
                    selected=False,
                    cells=[
                        ft.DataCell(ft.Text(response["id"])),
                        ft.DataCell(ft.Text(response["path"])),
                        ft.DataCell(delete_button)
                    ]

                ))
                origin_data_table.update()
                self.update()

        def delete_origin(e):
            number_of_rows = len(origin_data_table.rows)
            for row in origin_data_table.rows:
                if row.selected and number_of_rows > 1:
                    origin_id = row.cells[0].content.value
                    url = f"{url_base}/origins/{origin_id}"
                    requests.delete(url=url, headers=HEADERS)
                    origin_data_table.rows.remove(row)
                    self.update()

        all_origins = json.loads(requests.get(headers=HEADERS, url=f"{url_base}/origins/").text)
        delete_button = ft.IconButton(icon=ft.icons.DELETE, on_click=delete_origin)
        origin_data_table = ft.DataTable(
            show_checkbox_column=True,
            columns=[
                ft.DataColumn(ft.Text("#")),
                ft.DataColumn(ft.Text("Path")),
                ft.DataColumn(ft.Text("Delete"))
            ],
            rows=[
                ft.DataRow(on_select_changed=this_selected,
                           selected=False,
                           cells=[
                               ft.DataCell(ft.Text(item["id"])),
                               ft.DataCell(ft.Text(item["path"])),
                               ft.DataCell(delete_button)]) for item in all_origins["results"]

            ]
        )
        get_origin_directory_dialog = ft.FilePicker(on_result=get_directory_result)
        origin_text_field = ft.TextField(col=8, filled=True, disabled=True, border_radius=ft.border_radius.all(5),
                                         height=HEIGHT, text_size=SIZE)
        choose_new_origin_btn = ft.ElevatedButton("Choose New Origin", col=3, icon=ft.icons.FOLDER_OPEN, height=HEIGHT,
                                                  on_click=lambda _: get_origin_directory_dialog.get_directory_path(),
                                                  style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=5)))
        add_origin_btn = ft.IconButton(
            col=1,
            icon=ft.icons.ADD,
            height=HEIGHT,
            on_click=lambda _: add_origin(),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=5)
            )
        )

        return ft.ResponsiveRow(
            controls=[
                origin_text_field,
                add_origin_btn,
                choose_new_origin_btn,

                get_origin_directory_dialog,
                ft.Column(horizontal_alignment=ft.CrossAxisAlignment.STRETCH, col=12, height=150,
                          scroll=ft.ScrollMode.ALWAYS, controls=[origin_data_table])

            ]
        )
