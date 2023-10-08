import logging
import sys
from logging import Formatter, StreamHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
formatter = Formatter(
    '{asctime}, {levelname}, {message}', style='{'
)
handler.setFormatter(formatter)


class FailedRequestApi(Exception):
    """Исключение для неудачного запроса."""
    pass
