"""
Nozomi
URL Parameter Module
author: hugh@blinkybeach.com
"""
from typing import Any


class URLParameter:
    """A single URL parameter, e.g. beep=boop"""
    def __init__(
        self,
        key: str,
        value: Any
    ) -> None:

        assert isinstance(key, str)
        str(value)  # provoke error early
        self._key = key
        self._value = value

        return

    def __str__(self) -> str:
        return self._key + '=' + str(self._value)
