import json
import requests
from constants import HEADERS, url_base


class Service:

    @staticmethod
    def get_all_targets():
        return json.loads(requests.get(headers=HEADERS, url=f"{url_base}/targets/").text)

    @staticmethod
    def get_all_origins():
        return json.loads(requests.get(headers=HEADERS, url=f"{url_base}/origins/").text)

    @staticmethod
    def get_all_formats():
        return json.loads(requests.get(headers=HEADERS, url=f"{url_base}/formats/").text)

    @staticmethod
    def get_format_by_id(format_id: int):
        return json.loads(requests.get(headers=HEADERS, url=f"{url_base}/formats/{format_id}").text)

    @staticmethod
    def get_target_by_id(target_id: int):
        return json.loads(requests.get(headers=HEADERS, url=f"{url_base}/targets/{target_id}").text)

    @staticmethod
    def get_target_by_name(target_name: str):
        return json.loads(requests.get(headers=HEADERS, url=f"{url_base}/targets/{target_name}").text)

    @staticmethod
    def get_format_by_name(format_name: str):
        return json.loads(requests.get(headers=HEADERS, url=f"{url_base}/formats/{format_name}").text)

    @staticmethod
    def get_origin_by_path(origin_path: str):
        return json.loads(requests.get(headers=HEADERS, url=f"{url_base}/origins/{origin_path}").text)

    @staticmethod
    def add_format(format_name: str, target_id: int):
        return json.loads(
            requests.post(headers=HEADERS, url=f"{url_base}/formats/?name={format_name}&target_id={target_id}").text)

    @staticmethod
    def add_target(target_name: str, target_path: str):
        return json.loads(
            requests.post(headers=HEADERS, url=f"{url_base}/targets/?name={target_name}&path={target_path}").text)

    @staticmethod
    def add_origin(origin_path: str):
        return json.loads(requests.post(headers=HEADERS, url=f"{url_base}/origins/?path={origin_path}").text)

    @staticmethod
    def delete_origin(origin_id: int):
        return requests.delete(url=f"{url_base}/origins/{origin_id}", headers=HEADERS)

    @staticmethod
    def delete_format(format_id: int):
        return requests.delete(url=f"{url_base}/formats/{format_id}", headers=HEADERS)

    @staticmethod
    def delete_target(target_id: int):
        return requests.delete(url=f"{url_base}/targets/{target_id}", headers=HEADERS)

    @staticmethod
    def move_files(origin_id: int, origin_path: str):
        return json.loads(requests.post(url=f"{url_base}/move/?origin_id={origin_id}&origin_path={origin_path}").text)
