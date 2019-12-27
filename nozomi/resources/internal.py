"""
Nozomi
Internal Resource Module
Copyright Amatino Pty Ltd
"""
from nozomi.data.datastore import Datastore
from nozomi.security.internal_key import InternalKey
from nozomi.api.resource import Resource
from nozomi.http.query_string import QueryString
from nozomi.http.status_code import HTTPStatusCode
from nozomi.errors.error import NozomiError
from typing import Optional
from typing import Any


class InternalResource(Resource):
    """
    Abstract class defining an interface for API requests that
    must only be served to applications inside a pre-shared key boundary.
    For example, requests from a web application server to an API.
    """

    def __init__(
        self,
        datastore: Datastore,
        internal_key: InternalKey
    ) -> None:

        super().__init__(datastore)
        assert isinstance(internal_key, InternalKey)
        self._internal_key = internal_key
        return

    def serve(
        self,
        request_data: Optional[Any],
        request_arguments: Optional[QueryString],
        request_headers: QueryString
    ) -> str:

        if not self._internal_key.matches_headers(request_headers):
            raise NozomiError(
                'Not internally authorised',
                HTTPStatusCode.NOT_AUTHORISED
            )

        return super().serve(request_data, request_arguments, request_headers)
