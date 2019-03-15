"""
Nozomi
Resource Module
Copyright Amatino Pty Ltd
"""
from nozomi.http.arguments import HTTPArguments
from nozomi.http.headers import HTTPHeaders
from nozomi.data.datastore import Datastore
from nozomi.ancillary.immutable import Immutable
from nozomi.transmission.encodable import Encodable
from typing import Any
from typing import Optional


class Resource:
    """Abstract class defining machinery for responding to an API request"""

    def __init__(self, datastore: Datastore, debug: bool = False) -> None:
        assert isinstance(datastore, Datastore)
        self._datastore = datastore
        self._debug = debug
        return

    datastore = Immutable(lambda s: s._datastore)
    debug = Immutable(lambda s: s._debug)

    def compute_response(
        self,
        request_data: Optional[Any],
        request_arguments: Optional[HTTPArguments],
        request_headers: Optional[HTTPHeaders] = None
    ) -> Encodable:
        """Return serialisable response data"""
        raise NotImplementedError

    def serve(
        self,
        request_data: Any,
        request_arguments: Optional[HTTPArguments] = None,
        request_headers: Optional[HTTPHeaders] = None
    ) -> str:
        """Return a JSON-serialised response to a request"""
        return self.compute_response(
            request_data,
            request_arguments,
            request_headers
        ).serialise()
