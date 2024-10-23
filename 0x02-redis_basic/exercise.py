#!/usr/bin/env python3
"""This module create a Caxhe class, store data and return a string."""

import redis
import uuid
from typing import Union


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
