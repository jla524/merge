from typing import Optional
import requests
from merge import Config
from merge.common.helpers import JSON
from merge.logger.pkg_logger import Logger


class Ragic:
    __base_url = "https://na3.ragic.com"
    __headers = {"Authorization": f"Basic {Config.ragic_api_key()}"}

    @staticmethod
    def validate_data(data: JSON) -> bool:
        if not isinstance(data, dict):
            return False
        for key, value in data.items():
            if not (
                isinstance(key, (str, int))
                and isinstance(value, (str, int, float, list))
            ):
                return False
        return True

    def get_data(
        self, api_route: str, params: Optional[JSON] = None, timeout: int = 10
    ) -> requests.Response:
        if params and not self.validate_data(params):
            raise TypeError("Payload type check failed.")
        url = f"{self.__base_url}/{api_route}"
        response = requests.get(
            url, headers=self.__headers, params=params, timeout=timeout
        )
        return response

    def send_data(
        self, api_route: str, data: Optional[JSON] = None, timeout: int = 10
    ) -> requests.Response:
        if data is None:
            data = {}
        if not self.validate_data(data):
            raise TypeError("Payload type check failed.")
        url = f"{self.__base_url}/{api_route}"
        response = requests.post(
            url, headers=self.__headers, data=data, timeout=timeout
        )
        return response
