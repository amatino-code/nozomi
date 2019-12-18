"""
Nozomi
Nozomi rror Module
Copyright Amatino Pty Ltd
"""
from nozomi.http.status_code import HTTPStatusCode
from nozomi.ancillary.immutable import Immutable
import traceback


class NozomiError(Exception):

    def __init__(
        self,
        client_description: str,
        http_status_code: HTTPStatusCode
    ) -> None:
        if not isinstance(http_status_code, HTTPStatusCode):
            raise TypeError('status must be of type `HTTPStatusCode`')

        if not isinstance(client_description, str):
            raise TypeError('descriptions must be of type `str`')

        self._http_code = http_status_code
        self._client_description = client_description

        self._stack_trace = ''.join(traceback.format_exception(
            etype=type(self),
            value=self,
            tb=self.__traceback__
        ))

        super().__init__(client_description)
        return

    http_status_code = Immutable(lambda s: s._http)
    client_description = Immutable(lambda s: s._client_description)
    stack_trace = Immutable(lambda s: s._stack_trace)
