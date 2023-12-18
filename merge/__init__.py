from typing import Optional
from pathlib import Path
from dotenv import dotenv_values, find_dotenv


class Config:
    __package = "merge"
    __version = "0.0.1"
    __default_env = "dev"
    __config_dir = Path().home() / ".config" / __package
    __logfile_name = f"{__package}-{__version}.log"
    __config = dotenv_values(find_dotenv())
    __env = __config["APP_ENV"]
    __ragic_api_key = __config["RAGIC_API_KEY"]
    __ragic_attendance_route = "lynvolunteer/lyn-temp/9"
    __ragic_hours_detail_route = "lynvolunteer/lyn-temp/110"
    __ragic_live_hours_route = "lynvolunteer/lyn-temp/104"
    __otc_company_id = __config["OTC_COMPANY_ID"]
    __otc_developer_token = __config["OTC_DEVELOPER_TOKEN"]
    __otc_timecards_route = "t1QueryTimeCards"

    @classmethod
    def package(cls) -> str:
        return cls.__package

    @classmethod
    def version(cls) -> str:
        return cls.__version

    @classmethod
    def default_env(cls) -> str:
        return cls.__default_env

    @classmethod
    def config_dir(cls) -> Path:
        return cls.__config_dir

    @classmethod
    def logfile_name(cls) -> str:
        return cls.__logfile_name

    @classmethod
    def env(cls) -> Optional[str]:
        return cls.__env

    @classmethod
    def ragic_api_key(cls) -> Optional[str]:
        return cls.__ragic_api_key

    @classmethod
    def ragic_attendance_route(cls) -> str:
        return cls.__ragic_attendance_route

    @classmethod
    def ragic_hours_detail_route(cls) -> str:
        return cls.__ragic_hours_detail_route

    @classmethod
    def ragic_live_hours_route(cls) -> str:
        return cls.__ragic_live_hours_route

    @classmethod
    def otc_company_id(cls) -> Optional[str]:
        return cls.__otc_company_id

    @classmethod
    def otc_developer_token(cls) -> Optional[str]:
        return cls.__otc_developer_token

    @classmethod
    def otc_timecards_route(cls) -> Optional[str]:
        return cls.__otc_timecards_route
