"""
Nozomi
UserAgent Module
author: hugh@blinkybeach.com
"""
from nozomi.http.headers import Headers
from nozomi.ancillary.immutable import Immutable
from typing import TypeVar, Type

T = TypeVar('T', bound='UserAgent')


class UserAgent:

    def __init__(
        self,
        body: str
    ) -> None:

        self._body = body

        return

    string = Immutable(lambda s: s._body)

    @classmethod
    def from_headers(
        cls: Type[T],
        headers: Headers,
        fallback_to: str = 'Unavailable'
    ) -> T:

        body = headers.value_for('User-Agent')
        if body is None:
            return cls(body=fallback_to)

        return cls(body=body)
