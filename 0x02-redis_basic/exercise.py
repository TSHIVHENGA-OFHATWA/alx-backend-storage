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

    def get(self, id_key: str, fn: Callable = None,
            ) -> Union[str, bytes, int, float]:
        """Get data from Redis by key and convert data to desired format."""

        data = self.get(id_key)

        return fn(data) if fn is not None else data

    def gets_str(self, key: str) -> Optional[str]:
        """Get string data from redis"""

        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: int) -> Optional[int]:
        "Get integer data from redis"""

        return self.get(key, int)


def replay(fn: Callable) -> None:
    """Displays the history of calls of particular function"""

    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_storage = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_storage, redis.Redis):
        return
    f_name = fn.__qualname__
    input_keys = '{}:inputs'.format(f_name)
    output_keys = '{}:outputs'.format(f_name)
    call_count = 0
    if redis_storage.exists(f_name) != 0:
        call_count = int(redis_storage.get(f_name))
    print("{} was called {} times:".format(f_name, call_count))
    print(f"{f_name} was called {call_count} times:")
    inputs = redis_storage.lrange(input_keys, 0, -1)
    outputs = redis_storage.lrange(output_keys, 0, -1)
    for ingoin, outgoin in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(f_name, ingoin.decode("utf-8"),
                                     outgoin,))
