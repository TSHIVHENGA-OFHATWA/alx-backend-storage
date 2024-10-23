#!/usr/bin/env python3
"""This module create a Caxhe class, store data and return a string."""

import redis
import uuid
from typing import Union, Callable, Any, Optional


class Cache:
    """Class cache that store an instance of the Redis client"""

    def __init__(self):
        """Initialize the class and flush the instance"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the data in Redis and return a string"""

        id_key = str(uuid.uuid4())
        self._redis.set(id_key, data)
        return id_key

    def get(self, key: str, fn: Optional[Callable[[Any], Union[str, bytes, int, float]]] = None
            ) -> Optional[Union[str, bytes, int, float]]:
        """get data from Redis by key and convert data to desired format."""

        data = self._redis.get(key)

        return fn(data) if fn is not None else data

    def gets_str(self, key: str) -> Optional[str]:
        """get string data from redis"""

        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: int) -> Optional[int]:
        "get integer data from redis"""

        return self.get(key, int)
