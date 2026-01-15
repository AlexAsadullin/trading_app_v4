from datetime import datetime, timezone
from functools import lru_cache

import pytz

from .logging import setup_logger
from .settings import Settings

APP_ID = "sllr-cabinet-api"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


@lru_cache()
def get_tz() -> timezone:
    return pytz.timezone(settings.tz)


tz = get_tz()


def current_ts() -> int:
    return int(datetime.now(tz).timestamp() * 1000)


logger = setup_logger(settings.log_level, APP_ID)


__all__ = (
    "settings",
    "tz",
    "current_ts",
    "logger",
)
