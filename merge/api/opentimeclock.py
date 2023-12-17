from http import HTTPStatus
from datetime import datetime
import requests
from merge import Config
from merge.common.helpers import JSON


class OpenTimeClock:
    __base_url = "https://api1.opentimeclock.com/Jun-Inside-VPC?cmd=api"
    __credentials = {
        "companyId": Config.otc_company_id(), "developerToken": Config.otc_developer_token()
    }

    def get_data(self, api_route: str, params: JSON, timeout: int = 30) -> requests.Response:
        url = f"{self.__base_url}/{api_route}"
        response = requests.get(url, params={**self.__credentials, **params}, timeout=timeout)
        return response
