import asyncio
import logging
import flet as ft

from frontend.components.components import Title, ScreenContainer, FolderContainer, blue_folder_color, ListScroller, \
    SingleItemFileRow, PropertyColumn, Tag, BulletedItem

from frontend.controllers.screen_controller import ScreenController

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class FolderScreen(ft.UserControl):
    def __init__(self, col, screen_controller: ScreenController):
        super().__init__()
        self.controller = screen_controller
        self.file_title = None
        self.target_title = None
        self.origin_title = None
        self.title_divider = None
        self.target_list = None
        self.origin_list = None
        self.ellipsis_btn = None
        self.file_list = None
        self.format_section = None
        self.screen_frame = None
        self.main_column = None
        self.format_title = None
        self.all_origins = None
        self.all_targets = None
        self.all_formats = None
        self.property_column = None
        self.col = col
        self.screen_type = "folder"

    def get_data(self):
        try:
            self.all_targets = self.controller.get_targets()["results"]
            self.all_formats = self.controller.get_formats()["results"]
            self.all_origins = self.controller.get_origins()["results"]
        except Exception as e:
            logger.error(e)

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
                origin = self.controller.get_origin_by_name(folder_name)
                path = origin["path"]
                all_files = self.controller.get_origin_items(int(origin["id"]))
            elif tag == Tag.NEW_TARGET:
                target = self.controller.get_target_by_name(folder_name)
                path = target["path"]
                all_files = self.controller.get_target_items(int(target["id"]))
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
            self.screen_frame.controls.clear()
            logger.info(path)

            self.main_column.col = 9
            self.property_column = self.create_property_column(folder_name=folder_name, path=path,
                                                               format_section=format_section, e=e)
            self.screen_frame.controls.append(self.property_column)
            await self.rebuild_page(e)
        except Exception as e:
            logger.error(e)

    def create_property_column(self, e, folder_name, path, format_section):
        return PropertyColumn(folder_name=folder_name, path=path,
                              close_click=self.close_properties,
                              format_section=format_section)

    async def clear_page(self, e):
        self.screen_frame.controls.clear()
        self.file_list.controls.clear()

    async def rebuild_page(self, e):
        self.screen_frame.controls.insert(0, self.main_column)
        await self.update_async()

    async def close_properties(self, e):
        self.screen_frame.controls.clear()
        self.property_column = None
        self.main_column.col = 12
        self.screen_frame.controls.append(self.main_column)
        await self.update_async()

    def populate_folders(self, tag: Tag, folder_name: str, folder_id: int) -> FolderContainer:
        def open_properties(e):
            asyncio.create_task(self.show_properties_and_files(e, folder_name=folder_name, tag=tag))

        def delete(e):
            asyncio.create_task(self.delete_folder(e, folder_id=folder_id, tag=tag, name=folder_name))

        folder_params = {
            "folder_name": folder_name,
            "open_properties": open_properties,
            "on_delete": delete,
            "tag": tag
        }

        if tag != Tag.NEW_ORIGIN:
            folder_params["color"] = blue_folder_color

        return FolderContainer(**folder_params)

    async def delete_folder(self, e, folder_id: int, tag, name):
        logger.info(name)
        try:
            if tag == Tag.NEW_ORIGIN:
                response = self.controller.delete_origin(origin_id=folder_id)
                # TODO: set conditional logic to remove the control only if the response returns as valid
                self.origin_list.controls = [control for control in self.origin_list.controls if
                                             control.folder_name != name]
            else:
                response = self.controller.delete_target(target_id=folder_id)
                # TODO: set conditional logic to remove the control only if the response returns as valid
                self.target_list.controls = [control for control in self.target_list.controls if
                                             control.folder_name != name]
            await self.close_properties(e)
            await self.update_async()
        except Exception as e:
            logger.error(e)

    def get_components(self):
        self.format_title = Title("Folders", col=11)
        origin_controls = [
            self.populate_folders(tag=Tag.NEW_ORIGIN,
                                  folder_name=origin["name"],
                                  folder_id=origin["id"]
                                  ) for origin in self.all_origins] if self.all_origins else [ft.Text("None")]

        target_controls = [
            self.populate_folders(tag=Tag.NEW_TARGET,
                                  folder_name=target["name"],
                                  folder_id=target["id"]
                                  ) for target in self.all_targets] if self.all_targets else [ft.Text("None")]

        self.title_divider = ft.Divider(thickness=0.0, height=1, color=ft.colors.WHITE)
        self.origin_title = Title("Origins")
        self.origin_list = ft.Row(controls=origin_controls, scroll=ft.ScrollMode.AUTO)
        self.target_title = Title("Destinations")
        self.target_list = ft.Row(controls=target_controls, scroll=ft.ScrollMode.AUTO)
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

        self.screen_frame = ft.ResponsiveRow(
            col=12, controls=[
                self.main_column,
            ])

    def build(self):
        self.get_data()
        self.get_components()
        return ScreenContainer(
            content=self.screen_frame
        )
