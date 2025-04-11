import logging
import os
from typing import Any

from dotenv import load_dotenv

log = logging.getLogger(__name__)

load_dotenv()


def get_env(
    var: str,
    default: Any = None,
    cast: None | type = None,
    num_min: int | float | None = None,
    num_max: int | float | None = None,
) -> str | Any:
    """Return environment variable var value if it exists otherwise return default.

    :param var: environment variable to get
    :param default: default to return instead (defaults to None)
    :param cast: cast to type
    :param num_min: minimum number allowed. Applies only if cast: int|float.
    :param num_max: maximum number allowed. Applies only if cast: int|float.
    :return: environment variable value
    """
    sr = os.getenv(var)
    sr = sr if isinstance(sr, str) else default

    if cast is not None:
        try:
            if cast is bool:
                sr = sr.lower() in ("true", "1", "yes")
            else:
                sr = cast(sr)
            if cast in (int, float):
                if num_min is not None and sr < num_min:
                    log.warning(f"Value for {var} is below minimum; setting to {num_min}")
                    sr = cast(num_min)
                if num_max is not None and sr > num_max:
                    log.warning(f"Value for {var} is above maximum; setting to {num_max}")
                    sr = cast(num_max)
        except ValueError:
            log.error(f"Failed to cast {var} to {cast.__name__}")
            raise
    return sr


KRONOTERM_CLOUD_USER = get_env("KRONOTERM_CLOUD_USER")
KRONOTERM_CLOUD_PASSWORD = get_env("KRONOTERM_CLOUD_PASSWORD")

PROMETHEUS_UPDATE_INTERVAL = get_env("PROMETHEUS_UPDATE_INTERVAL", 30, cast=int, num_min=10)

log.info("PROMETHEUS_UPDATE_INTERVAL=%s", PROMETHEUS_UPDATE_INTERVAL)
log.info("TZ=%s", get_env("TZ"))
