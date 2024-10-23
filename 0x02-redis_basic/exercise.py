#!/usr/bin/env python3
"""This module create a Caxhe class, store data and return a string."""

import redis
import uuid
from typing import Union, Callable, Any, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Tracks number of calls made to a method in a Cache class
        and return a callable wrapped method"""

    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Invokes given method after incrementing its call counter
            and return any results of the method call.
        """

        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


def call_history(method: Callable) -> Callable:
    """Tracks calls details of method in class Cache."""

    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        """Return method output after storing data."""

        input_key = '{}:inputs'.format(method.__qualname__)
        output_key = '{}:outputs'.format(method.__qualname__)

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))

        result = method(self, *args, **kwargs)

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(output_key, result)

        return result
    return invoker


class Cache:
    """Class cache that store an instance of the Redis client"""

    def __init__(self):
        """Initialize the class and flush the instance"""

        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the data in Redis and return a string"""

        id_key = str(uuid.uuid4())
        self._redis.set(id_key, data)
        return id_key

    def get(self, key: str, fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """get data from Redis by key and convert data to desired format."""

        data = self._redis.get(key)

        return fn(data) if fn is not None else data

    def gets_str(self, key: str) -> Optional[str]:
        """get string data from redis"""

        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: int) -> Optional[int]:
        "get integer data from redis"""

        return self.get(key, int)
