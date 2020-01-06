"""
Nozomi
Secure Resource Module
author: hugh@blinkybeach.com
"""
from nozomi.errors.error import NozomiError
from nozomi.app.security.session import Session
from nozomi.security.agent import Agent
from nozomi.resources.resource import Resource
from nozomi.http.query_string import QueryString
from nozomi.http.status_code import HTTPStatusCode
from nozomi.http.parseable_data import ParseableData
from nozomi.http.headers import Headers
from nozomi.data.encodable import Encodable
from typing import Optional


class OpenResource(Resource):
    """
    Abstract class defining an interface for for resources that do not require
    authentication, but that are aware of a requesting agent. For example, a web
    page that may be served differently depending on whether a user is logged in
    or not.
    """

    def compute_response(
        self,
        request_data: Optional[ParseableData],
        request_arguments: Optional[QueryString],
        requesting_agent: Agent
    ) -> Encodable:
        """
        Method returning a Broadcastable response, and an Agent authorised to
        make the request
        """
        raise NotImplementedError

    def serve(
        self,
        request_data: Optional[ParseableData],
        request_arguments: Optional[QueryString],
        headers: Headers
    ) -> str:
        session = Session.from_headers(
            headers=headers,
            datastore=self.datastore,
            configuration=self.configuration
        )
        if session is None:
            raise NozomiError(
                'Not authenticated',
                HTTPStatusCode.NOT_AUTHENTICATED
            )
        response = self.compute_response(
            request_data,
            request_arguments,
            session
        )

        return response.serialise()
