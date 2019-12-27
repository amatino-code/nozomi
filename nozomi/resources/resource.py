"""
Nozomi
Resource Module
Copyright Amatino Pty Ltd
"""
from nozomi.http.query_string import QueryString
from nozomi.http.query_string import QueryString
from nozomi.data.datastore import Datastore
from nozomi.ancillary.immutable import Immutable
from nozomi.data.encodable import Encodable
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
        request_arguments: Optional[QueryString],
        request_headers: Optional[QueryString] = None
    ) -> Encodable:
        """Return serialisable response data"""
        raise NotImplementedError

    def serve(
        self,
        request_data: Any,
        request_arguments: Optional[QueryString] = None,
        request_headers: Optional[QueryString] = None
    ) -> str:
        """Return a string response body to a request"""
        return self.compute_response(
            request_data,
            request_arguments,
            request_headers
        ).serialise()
