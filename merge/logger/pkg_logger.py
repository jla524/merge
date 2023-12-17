import sys
import logging
from logging.config import dictConfig
from pathlib import Path
from colorama import init, Back, Fore
from merge import Config
from merge.logger import LOGGING_CONFIG

init(autoreset=True)


class LoggerLoader:
    def __init__(self):
        self.__log_dump: Path = Config.config_dir()
        self.__load_config()

    def __load_config(self):
        # If dump site doesn't exist, create it with all parent folders leading up to it
        if not self.__log_dump.is_dir():
            self.__log_dump.mkdir(parents=True)

        try:
            # If syntax is wrong, logging module will raise ValueError
            dictConfig(LOGGING_CONFIG)
        except ValueError as error:
            sys.stderr.write(
                f"{Fore.RED}Loading default logging config failed, syntax error\n\n{error}"
            )
            sys.exit(1)
        except KeyError as error:
            sys.stderr.write(
                f"{Fore.RED}Loading logging config failed, syntax error\n\n{error}"
            )
            sys.exit(1)

    @staticmethod
    def load() -> logging.Logger:
        # first test to see if the name is a valid defined logger name
        valid: bool = False
        try:
            for logger_name in LOGGING_CONFIG["loggers"]:
                if logger_name == Config.env():
                    valid = True
        except KeyError as error:
            sys.stderr.write(f"{error}")

        if not valid:
            # name passed is not a valid listed logger, return dev as default logger
            sys.stderr.write(
                f"\n{Back.BLACK}{Fore.RED}{Config.env()}: "
                "IS NOT A VALID LOGGER\n"
                f"{Back.BLACK}{Fore.YELLOW}FALLING BACK TO "
                f"{Config.default_env()}\n"
            )
            logger = logging.getLogger(Config.default_env())
            return logger

        logger = logging.getLogger(Config.env())
        return logger


class Logger:
    __logger = LoggerLoader().load()

    @classmethod
    def debug(cls, msg: str):
        cls.__logger.debug(msg)

    @classmethod
    def info(cls, msg: str):
        cls.__logger.info(msg)

    @classmethod
    def warn(cls, msg: str):
        cls.__logger.warning(msg)

    @classmethod
    def error(cls, msg: str):
        cls.__logger.error(msg)
