import logging

import colorlog

logger = logging.getLogger('custom_logger')
logger.setLevel(logging.DEBUG)
formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s %(levelname)s: %(message)s',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    },
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
