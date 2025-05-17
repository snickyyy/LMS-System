import logging

import settings.settings


def configure_logger() -> None:
    s = settings.settings.get_settings().LOGGING
    logging.basicConfig(
        level=s.LOGS_LEVEL,
        format=s.LOGS_FORMAT,
        datefmt=s.LOGS_DATEFORMAT,
    )
