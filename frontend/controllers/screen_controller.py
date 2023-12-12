import logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(funcName)s : %(message)s")
logger = logging.getLogger(__name__)


class ScreenController:
    def __init__(self, service):
        self.service = service

    def move_files(self, origin_id, origin_path):
        try:
            return self.service.move_files(origin_id=origin_id, origin_path=origin_path)
        except Exception as e:
            logger.error(e)

    def get_format_by_name(self, format_name: str):
        try:
            return self.service.get_format_by_name(format_name)
        except Exception as e:
            logger.error(e)

    def get_formats(self):
        try:
            return self.service.get_all_formats()
        except Exception as e:
            logger.error(e)

    def add_format(self, format_name, target_id):
        try:
            return self.service.add_format(format_name=format_name,
                                           target_id=target_id)
        except Exception as e:
            logger.error(e)

    def delete_format(self, format_id: int):
        try:
            return self.service.delete_format(format_id)
        except Exception as e:
            logger.error(e)

    def get_target_by_name(self, target_name: str):
        try:
            return self.service.get_target_by_name(target_name)
        except Exception as e:
            logger.error(e)

    def get_targets(self):
        try:
            return self.service.get_all_targets()
        except Exception as e:
            logger.error(e)

    def get_target_by_id(self, target_id: int):
        try:
            return self.service.get_target_by_id(target_id)
        except Exception as e:
            logger.error(e)

    def get_origin_by_name(self, origin_name: str):
        try:
            return self.service.get_origin_by_name(origin_name)
        except Exception as e:
            logger.error(e)

    def get_origins(self):
        try:
            return self.service.get_all_origins()
        except Exception as e:
            logger.error(e)

    def get_origin_items(self, origin_id: int):
        try:
            return self.service.get_origin_items(origin_id)
        except Exception as e:
            logger.error(e)

    def get_origin_by_id(self, origin_id: int):
        try:
            return self.service.get_origin_by_id(origin_id)
        except Exception as e:
            logger.error(e)

    def delete_origin(self, origin_id: int):
        try:
            return self.service.delete_origin(origin_id)
        except Exception as e:
            logger.error(e)

    def delete_target(self, target_id: int):
        try:
            return self.service.delete_target(target_id)
        except Exception as e:
            logger.error(e)

    def delete_targets(self, target_id: int):
        try:
            return self.service.delete_target(target_id)
        except Exception as e:
            logger.error(e)

    def get_target_items(self, target_id: int):
        try:
            return self.service.get_target_items(target_id)
        except Exception as e:
            logger.error(e)
