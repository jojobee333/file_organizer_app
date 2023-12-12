import requests
from constants import HEADERS, url_base


class Service:

    @staticmethod
    def get_all_targets():
        response = requests.get(headers=HEADERS, url=f"{url_base}/targets/")
        return response.json()

    @staticmethod
    def get_all_origins():
        response = requests.get(headers=HEADERS, url=f"{url_base}/origins/")
        return response.json()

    @staticmethod
    def get_all_formats():
        response = requests.get(headers=HEADERS, url=f"{url_base}/formats/")
        return response.json()

    @staticmethod
    def get_format_by_id(format_id: int):
        response = requests.get(headers=HEADERS, url=f"{url_base}/formats/{format_id}")
        return response.json()

    @staticmethod
    def get_target_by_id(target_id: int):
        response = requests.get(headers=HEADERS, url=f"{url_base}/targets/{target_id}")
        return response.json()

    @staticmethod
    def get_origin_by_id(origin_id: int):
        response = requests.get(headers=HEADERS, url=f"{url_base}/origins/{origin_id}")
        return response.json()

    @staticmethod
    def get_target_by_name(target_name: str):
        response = requests.get(headers=HEADERS, url=f"{url_base}/targets/{target_name}")
        return response.json()

    @staticmethod
    def get_format_by_name(format_name: str):
        response = requests.get(headers=HEADERS, url=f"{url_base}/formats/{format_name}")
        return response.json()

    @staticmethod
    def get_origin_by_path(origin_path: str):
        response = requests.get(headers=HEADERS, url=f"{url_base}/origins/{origin_path}")
        return response.json()

    @staticmethod
    def get_origin_by_name(origin_name: str):
        response = requests.get(headers=HEADERS, url=f"{url_base}/origins/{origin_name}")
        return response.json()

    @staticmethod
    def get_origin_items(origin_id: int):
        response = requests.get(headers=HEADERS, url=f"{url_base}/origins/{origin_id}/items")
        return response.json()

    @staticmethod
    def get_target_items(target_id: int):
        response = requests.get(headers=HEADERS, url=f"{url_base}/targets/{target_id}/items")
        return response.json()

    @staticmethod
    def add_format(format_name: str, target_id: int):
        response = requests.post(headers=HEADERS,
                                 url=f"{url_base}/formats/?name={format_name}&target_id={target_id}")
        return response.json()

    @staticmethod
    def add_target(target_name: str, target_path: str):
        response = requests.post(headers=HEADERS,
                                 url=f"{url_base}/targets/?name={target_name}&path={target_path}")
        return response.json()

    @staticmethod
    def add_origin(origin_name: str, origin_path: str):
        response = requests.post(headers=HEADERS,
                                 url=f"{url_base}/origins/?name={origin_name}&path={origin_path}")
        return response.json()

    @staticmethod
    def delete_origin(origin_id: int):
        response = requests.delete(url=f"{url_base}/origins/{origin_id}", headers=HEADERS)
        return response.json()

    @staticmethod
    def delete_format(format_id: int):
        response = requests.delete(url=f"{url_base}/formats/{format_id}", headers=HEADERS)
        return response.json()

    @staticmethod
    def delete_target(target_id: int):
        response = requests.delete(url=f"{url_base}/targets/{target_id}", headers=HEADERS)
        return response.json()

    @staticmethod
    def move_files(origin_id: int, origin_path: str):
        url = f"{url_base}/run/?origin_id={origin_id}&origin_path={origin_path}"
        response = requests.post(url=url)
        return response.json()
