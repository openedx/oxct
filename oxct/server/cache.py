import importlib
import json
import logging
import os
from random import randint
from time import sleep

from typing import Any, Iterable, Optional

import redis


logger = logging.getLogger(__name__)


class Cache:
    INSTANCE: Optional[redis.Redis] = None
    MIN_TTL_SECONDS = 10
    MAX_TTL_SECONDS = 24 * 3600

    def __init__(self):
        self.redis_client = redis.Redis(
            host=os.environ.get("OXCT_REDIS_HOST", "127.0.0.1"),
            port=int(os.environ.get("OXCT_REDIS_PORT", "6379")),
            db=int(os.environ.get("OXCT_REDIS_DB", "0")),
        )

    @classmethod
    def instance(cls) -> redis.Redis:
        if cls.INSTANCE is None:
            cls.INSTANCE = cls()
        return cls.INSTANCE

    def clear(self):
        self.redis_client.flushdb()

    def get(self, key: str) -> Optional[Any]:
        serialized_key = serialize(key)
        value = self.redis_client.get(serialized_key)
        if value is None:
            logger.info("Cache miss: '%s'", serialized_key)
            return None
        logger.info("Cache hit: '%s'", serialized_key)
        return deserialize(value)

    def set(self, key: Any, value: Any) -> None:
        ttl = randint(self.MIN_TTL_SECONDS, self.MAX_TTL_SECONDS)
        serialized_key = serialize(key)
        logger.info("Set cache (ttl=%d): '%s'", ttl, serialized_key)
        self.redis_client.set(serialized_key, serialize(value), ex=ttl)

    def iter_expired_keys(self) -> Iterable[Any]:
        pubsub = self.redis_client.pubsub()
        pubsub.psubscribe("__key*__:expired")
        while True:
            message = pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                serialized_key = message["data"].decode()
                logger.info("Key expiry: %s", serialized_key)
                key = deserialize(serialized_key)
                yield key
            sleep(0.1)


def memoize(func):
    def decorated(*args, **kwargs):
        key = {
            "module": func.__module__,
            "name": func.__name__,
            "args": list(args),
            "kwargs": kwargs,
        }
        cache = Cache.instance()
        value = cache.get(key)
        if value is None:
            value = func(*args, **kwargs)
            cache.set(key, value)
        return value

    return decorated


def serialize(data: Any) -> str:
    return json.dumps(
        data,
        sort_keys=True,
    )


def deserialize(content: str) -> Any:
    return json.loads(content)


def recompute_expired(count=None):
    """
    Recompute memoized function calls as soon as they expire.

    Args:
        count (int): stop after recomputing this many calls.
    """
    recomputed_count = 0
    for key in Cache.instance().iter_expired_keys():
        if count is not None and recomputed_count >= count:
            break
        module = importlib.import_module(key["module"])
        func = getattr(module, key["name"])
        # TODO do not fail on import error?
        func(*key["args"], **key["kwargs"])
        recomputed_count += 1
