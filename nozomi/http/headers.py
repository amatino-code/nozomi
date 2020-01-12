"""
Nozomi
HTTP Headers Module
Copyright Amatino Pty Ltd
"""
from typing import Optional, List
from collections.abc import Mapping
from nozomi.errors.error import NozomiError
from nozomi.http.status_code import HTTPStatusCode


class Headers:
    """
    A set of HTTP headers. Feed Headers a Mapping-conformant data type, for
    example a Dict or a Werkzeug ImmutableMultiDict.
    """

    def __init__(self, raw: Mapping) -> None:
        self._raw = raw
        return

    def value_for(self, key: str) -> Optional[str]:
        """
        Return the value of a supplied header key, or None if no value
        exists for that key.
        """
        value = self._raw.get(key)
        if value is None:
            return None

        if not isinstance(value, str):
            raise NozomiError('The data structure underlying a Headers instance\
unexpectedly contained non-string data for key "{k}", of type {t}. Headers \
must only contain string values. Consider examining the data you fed to the \
Headers initialiser.', HTTPStatusCode.BAD_REQUEST)

        return value

    def getlist(self, key: str) -> List[str]:

        if not hasattr(self._raw, 'getlist'):
            return list()

        return self._raw.getlist(key)

    def add(self, key: str, value: str) -> None:
        self._raw.add(key, value)
        return
