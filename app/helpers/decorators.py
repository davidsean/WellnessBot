import os
import logging
from typing import Callable


CHANNEL = os.getenv('CHANNEL_ID')

_log = logging.getLogger(__name__)


def in_wellness_channel(func: Callable):
    async def wrapper(*args, **kwargs):
        if CHANNEL is None or args[0].channel.id == int(CHANNEL):
            await func(*args, **kwargs)
        else:
            _log.info("Command not in wellness channel")
    return wrapper


def log_user(func: Callable):
    async def wrapper(*args, **kwargs):
        _log.info("Command: %s invoked by user: %s", func.__name__, args[0].author)
        await func(*args, **kwargs)
    return wrapper
