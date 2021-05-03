import json
import logging
import os
import sys
from datetime import timedelta
from pathlib import Path
from types import FrameType
from typing import Callable, Optional, TypedDict, Union

import loguru
from loguru import logger


class Logging_Config_Data(TypedDict):
    level: str
    format: str
    path: Union[Path, str]
    retention: Optional[timedelta]
    rotation: Optional[timedelta]


config: Logging_Config_Data = {
    "level": "trace",
    "format": (
        "<level>{level:8}</level> | "
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<cyan>{name:35}</cyan>:<cyan>{function:30}</cyan>:<cyan>{line:4}</cyan> | "
        "<level>{message: <8}</level>"
    ),
    "path": os.environ.get("LOG_PATH", "log.txt"),
    "retention": timedelta(days=7),
    "rotation": None,
}


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        log = logger.bind(request_id="app")
        log.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def make_logger() -> "loguru.Logger":

    logger = customize_logging(
        config.get("path"),
        level=config["level"],
        retention=config.get("retention"),
        rotation=config.get("rotation"),
        format=config["format"],
    )
    return logger


def customize_logging(
    filepath: Optional[Union[Path, str]],
    level: str,
    rotation: Optional[timedelta],
    retention: Optional[timedelta],
    format: str,
) -> "loguru.Logger":

    logger.remove()
    logger.add(
        sink=sys.stdout,
        enqueue=True,
        backtrace=True,
        level=level.upper(),
        format=format,
    )

    logger.level("TRACE", color="<green><d>")

    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    for _log in ["uvicorn", "uvicorn.error", "fastapi"]:
        _logger = logging.getLogger(_log)
        _logger.handlers = [InterceptHandler()]

    return logger.bind(request_id=None, method=None)
