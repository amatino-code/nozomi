"""
Nozomi
Nozomi rror Module
Copyright Amatino Pty Ltd
"""
import datetime
from nozomi.http.status_code import HTTPStatusCode
from collections.abc import Mapping
from nozomi.ancillary.immutable import Immutable
from nozomi.data.encodable import Encodable
from typing import Optional, Any, Dict, Union
import traceback


class NozomiError(Exception):

    def __init__(
        self,
        client_description: str,
        http_status_code: Union[HTTPStatusCode, int, str]
    ) -> None:

        if not isinstance(http_status_code, HTTPStatusCode):

            try:
                http_status_code = HTTPStatusCode(int(http_status_code))
            except Exception:
                raise TypeError('status must be a valid `HTTPStatusCode`')

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

    http_status_code = Immutable(lambda s: s._http_code)
    client_description = Immutable(lambda s: s._client_description)
    stack_trace = Immutable(lambda s: s._stack_trace)
    info_package = Immutable(lambda s: s._info_package())
    is_500_class = Immutable(lambda s: str(s._http_code.value)[0] == '5')

    def _info_package(self) -> Dict[str, Any]:
        """
        Return a package of information an application can parse to
        learn more about the error
        """
        data = {
            'error-information': self.client_description,
            'response-code': self.http_status_code.value
        }
        return NozomiError._InfoPackage(data)

    def report(
        self,
        request_headers: Optional[Mapping] = None,
        request_json: Optional[Any] = None,
        request_arguments: Optional[Any] = None
    ) -> str:
        """
        Return human-readable a string describing the error, including
        a traceback
        """
        report = '\n\n--##-- Procuret API Error Report --##--\n'
        report += str(datetime.datetime.utcnow()) + ' UTC\n'
        report += 'Exception: ' + str(self) + '\n'
        report += '--//-- Begin traceback --//--\n\n'
        trace = traceback.format_tb(self.__traceback__)
        for line in trace:
            report += line
        report += '\n--//-- End traceback --//--\n'
        report += '\nRequest headers: \n'
        report += str(request_headers)
        report += '\nRequest JSON: \n'
        report += str(request_json)
        report += '\nRequest arguments:\n'
        report += str(request_arguments)
        report += '\n--##-- End Error Report --##--\n'
        return report

    class _InfoPackage(Encodable):
        def __init__(self, data: Dict[str, Any]) -> None:
            self._data = data
            return

        def encode(self) -> Dict[str, Any]:
            return self._data
