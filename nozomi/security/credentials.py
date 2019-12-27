"""
Nozomi
Credentials Module
author: hugh@blinkybeach.com
"""
from nozomi.ancillary.immutable import Immutable
from nozomi.http.headers import Headers
from typing import Type, TypeVar, Optional

T = TypeVar('T', bound='Credentials')


class Credentials:
    """An instance of credentials sent by a client in their HTTP headers"""

    API_KEY_NAME = NotImplemented
    SESSION_ID_NAME = NotImplemented

    def __init__(
        self,
        session_id: str,
        api_key: str
    ) -> None:

        assert isinstance(session_id, str)
        assert isinstance(api_key, str)

        self._session_id = session_id
        self._api_key = api_key

        return

    api_key = Immutable(lambda s: s._api_key)
    session_id = Immutable(lambda s: s._session_id)

    @classmethod
    def from_headers(cls: Type[T], headers: Headers) -> Optional[T]:
        """Extract credentials from request headers"""

        session_id = headers.get(cls.SESSION_ID_NAME, default=None)
        if session_id is None:
            return None

        api_key = headers.get(cls.API_KEY_NAME, default=None)
        if api_key is None:
            return None

        return cls(session_id, api_key)
