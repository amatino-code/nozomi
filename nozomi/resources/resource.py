"""
Nozomi
Resource Module
Copyright Amatino Pty Ltd
"""
from nozomi.http.query_string import QueryString
from nozomi.http.parseable_data import ParseableData
from nozomi.http.headers import Headers
from nozomi.data.datastore import Datastore
from nozomi.ancillary.immutable import Immutable
from nozomi.data.encodable import Encodable
from nozomi.ancillary.configuration import Configuration
from typing import Any
from typing import Optional


class Resource:
    """Abstract class defining machinery for responding to an API request"""

    def __init__(
        self,
        datastore: Datastore,
        configuration: Configuration
    ) -> None:
        assert isinstance(datastore, Datastore)
        self._datastore = datastore
        self._debug = configuration.debug
        self._configuration = configuration
        return

    datastore = Immutable(lambda s: s._datastore)
    debug = Immutable(lambda s: s._debug)
    configuration = Immutable(lambda s: s._configuration)

    def compute_response(
        self,
        request_data: Optional[Any],
        request_arguments: Optional[QueryString],
        headers: Optional[Headers] = None
    ) -> Encodable:
        """Return serialisable response data"""
        raise NotImplementedError

    def serve(
        self,
        request_data: Optional[ParseableData],
        request_arguments: Optional[QueryString] = None,
        request_headers: Optional[Headers] = None
    ) -> str:
        """Return a string response body to a request"""
        return self.compute_response(
            request_data,
            request_arguments,
            request_headers
        ).serialise()
