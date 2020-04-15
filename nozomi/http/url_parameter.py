"""
Nozomi
URL Parameter Module
author: hugh@blinkybeach.com
"""
from typing import Any
from nozomi.ancillary.immutable import Immutable


class URLParameter:
    """A single URL parameter, e.g. beep=boop"""
    def __init__(
        self,
        key: str,
        value: Any
    ) -> None:

        assert isinstance(key, str)
        if isinstance(value, bool):
            value = str(value).lower()
        str(value)  # provoke error early
        self._key = key
        self._value = value

        return

    key: str = Immutable(lambda s: s._key)

    def __str__(self) -> str:
        return self._key + '=' + str(self._value)
