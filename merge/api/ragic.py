from http import HTTPStatus
import requests
from merge import Config
from merge.common.helpers import JSON
from merge.logger.pkg_logger import Logger


class Ragic:
    __base_url = "https://na3.ragic.com"
    __headers = {"Authorization": f"Basic {Config.ragic_api_key()}"}

    def get_data(self, api_route: str, params: JSON = {}, timeout: int = 10) -> requests.Response:
        url = f"{self.__base_url}/{api_route}"
        response = requests.get(url, headers=self.__headers, params=params, timeout=timeout)
        return response

    def send_data(self, api_route: str, data: JSON = {}, timeout: int = 10) -> requests.Response:
        url = f"{self.__base_url}/{api_route}"
        response = requests.post(url, headers=self.__headers, data=data, timeout=timeout)
        return response
