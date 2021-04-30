import logging
import sys
from pathlib import Path
from loguru import logger
from loguru import _Logger as Logger
import json
from datetime import timedelta
import os

logging_config = {
    "level": "trace",
    "format": (
        "<level>{level:8}</level> | "
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<cyan>{name:35}</cyan>:<cyan>{function:30}</cyan>:<cyan>{line:4}</cyan> | "
        "<level>{message: <8}</level>"
    ),
    "path": os.environ.get('LOG_PATH', 'log.txt'),
    "retention": timedelta(days=7)
}

class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record) -> None:
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind(request_id='app')
        log.opt(
            depth=depth,
            exception=record.exc_info
        ).log(level,record.getMessage())


def make_logger() -> Logger:

    logger = customize_logging(
        logging_config.get('path'),
        level=logging_config.get('level'),
        retention=logging_config.get('retention'),
        rotation=logging_config.get('rotation'),
        format=logging_config.get('format')
    )
    return logger

def customize_logging(
        filepath: Path,
        level: str,
        rotation: str,
        retention: str,
        format: str
) -> Logger:

    logger.remove()
    logger.add(
        sys.stdout,
        enqueue=True,
        backtrace=True,
        level=level.upper(),
        format=format
    )

    logger.level("TRACE", color="<green><d>")

    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    for _log in ['uvicorn',
                    'uvicorn.error',
                    'fastapi'
                    ]:
        _logger = logging.getLogger(_log)
        _logger.handlers = [InterceptHandler()]

    return logger.bind(request_id=None, method=None)