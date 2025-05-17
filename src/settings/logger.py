import logging

import settings.settings


def configure_logger() -> None:
    s = settings.settings.get_settings().LOGGING
    logging.basicConfig(
        level=s.LOGGING.LOGS_LEVEL,
        format=s.LOGGING.LOGS_FORMAT,
        datefmt=s.LOGGING.LOGS_DATEFORMAT,
    )
