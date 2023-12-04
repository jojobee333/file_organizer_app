import asyncio
import logging

import flet as ft

from backend.service import Service
from frontend.components.components import Title, ScreenContainer, FolderContainer, blue_folder_color, ListScroller, \
    SingleItemFileRow, PropertyColumn, Tag, CloseButton, BulletedItem

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class FolderScreen(ft.UserControl):
    def __init__(self, col):
        super().__init__()
        self.file_title = None
        self.target_title = None
        self.origin_title = None
        self.title_divider = None
        self.target_list = None
        self.origin_list = None
        self.ellipsis_btn = None
        self.file_list = None
        self.format_section = None
        self.screen_row = None
        self.main_column = None
        self.format_title = None
        self.all_origins = None
        self.all_targets = None
        self.all_formats = None
        self.property_column = None
        self.col = col
        self.screen_type = "folder"

    def get_data(self):
        self.all_targets = Service().get_all_targets()["results"]
        self.all_formats = Service().get_all_formats()["results"]
        self.all_origins = Service().get_all_origins()["results"]

    @staticmethod
    def populate_files(name, location):
        return SingleItemFileRow(name=name, location=location)

    async def show_properties_and_files(self, e, folder_name, tag):
        try:
            path = None
            all_files = None
            format_section = ft.Text("")
            self.file_list.controls.clear()

            if tag == Tag.NEW_ORIGIN:
                origin = Service.get_origin_by_name(folder_name)
                path = origin["path"]
                all_files = Service.get_origin_items(int(origin["id"]))
            elif tag == Tag.NEW_TARGET:
                target = Service.get_target_by_name(folder_name)
                path = target["path"]
                all_files = Service.get_target_items(int(target["id"]))
                target_formats = [fmt for fmt in self.all_formats if fmt["target_id"] == target["id"]]
                format_section = ft.Column(
                    controls=[Title("Formats"),
                              self.title_divider,
                              ListScroller(
                                  controls=[BulletedItem(item_name=fmt["name"]) for fmt in target_formats])])

            if not path:
                raise Exception
            if all_files:
                self.file_list.controls = [FolderScreen.populate_files(name=file, location=folder_name) for file in
                                           all_files]
            else:
                self.file_list.controls.clear()
            self.screen_row.controls.clear()
            logger.info(path)

            self.main_column.col = 9
            self.property_column = self.create_property_column(folder_name=folder_name, path=path,
                                                               format_section=format_section, e=e)
            self.screen_row.controls.append(self.property_column)
            await self.rebuild_page(e)
        except Exception as e:
            logger.error(e)

    def create_property_column(self, e, folder_name, path, format_section):
        return PropertyColumn(folder_name=folder_name, path=path,
                              delete_click=self.close_properties,
                              format_section=format_section)

    async def clear_page(self, e):
        self.screen_row.controls.clear()
        self.file_list.controls.clear()

    async def rebuild_page(self, e):
        self.screen_row.controls.insert(0, self.main_column)
        await self.update_async()

    async def close_properties(self, e):
        self.screen_row.controls.clear()
        self.property_column = None
        self.main_column.col = 12
        self.screen_row.controls.append(self.main_column)
        await self.update_async()

    def populate_folders(self, tag: Tag, folder_name: str, delete_btn=None) -> FolderContainer:
        def on_click(e):
            asyncio.create_task(self.show_properties_and_files(e, folder_name=folder_name, tag=tag))

        folder_params = {
            "folder_name": folder_name,
            "on_click": on_click,
            "tag": tag
        }

        if tag != Tag.NEW_ORIGIN:
            folder_params["color"] = blue_folder_color

        if delete_btn:
            folder_params["delete_btn"] = delete_btn

        return FolderContainer(**folder_params)

    async def delete_folder(self, e, tag):
        try:
            response = None
        except Exception as e:
            logger.error(e)

    def get_components(self):
        self.format_title = Title("Folders", col=11)
        origin_controls = [
            self.populate_folders(tag=Tag.NEW_ORIGIN, folder_name=origin["name"]) for origin in
            self.all_origins] if self.all_origins else [ft.Text("None")]

        target_controls = [
            self.populate_folders(tag=Tag.NEW_TARGET, folder_name=target["name"]) for target in
            self.all_targets] if self.all_targets else [ft.Text("None")]

        self.title_divider = ft.Divider(thickness=0.0, height=1, color=ft.colors.WHITE)
        self.origin_title = Title("Origins")
        self.origin_list = ft.Row(controls=origin_controls)
        self.target_title = Title("Destinations")
        self.target_list = ft.Row(controls=target_controls)
        self.file_title = Title("Files")
        self.file_list = ListScroller(controls=[])

        self.main_column = ft.SafeArea(
            col=12,
            minimum=10,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                col=12,
                controls=[
                    self.format_title,
                    self.title_divider,
                    self.origin_title,
                    self.origin_list,
                    self.target_title,
                    self.target_list,
                    self.file_title,
                    self.file_list

                ]))

        self.screen_row = ft.ResponsiveRow(controls=[
            self.main_column,
        ])

    def build(self):
        self.get_data()
        self.get_components()

        return ScreenContainer(
            content=self.screen_row
        )
