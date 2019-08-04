import logging
from df_backend import __name__ as logger_name

from . import constants


def setup_logging(level=logging.DEBUG):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(level)

    return logger


__all__ = ['setup_logging', 'constants']