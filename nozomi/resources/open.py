"""
Nozomi
Secure Resource Module
author: hugh@blinkybeach.com
"""
from typing import Any
from nozomi.errors.error import NozomiError
from nozomi.security.broadcastable import Broadcastable
from nozomi.security.session import Session
from nozomi.security.agent import Agent
from nozomi.resources.resource import Resource
from nozomi.http.query_string import QueryString
from nozomi.http.status_code import HTTPStatusCode
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
        request_data: Optional[Any],
        request_arguments: Optional[QueryString],
        requesting_agent: Agent
    ) -> Broadcastable:
        """
        Method returning a Broadcastable response, and an Agent authorised to
        make the request
        """
        raise NotImplementedError

    def serve(
        self,
        request_data: Optional[Any],
        request_arguments: Optional[QueryString],
        headers: QueryString
    ) -> str:
        session = Session.from_headers(
            hedaers=headers,
            datastore=self.datastore,
            configuration=self.configuration
        )
        if session is None:
            raise NozomiError(
                'Not authenticated',
                HTTPStatusCode.NOT_AUTHENTICATED
            )
        response, authorised_agent = self.compute_response(
            request_data,
            request_arguments,
            session.human
        )
        if not isinstance(authorised_agent, Agent):
            raise RuntimeError('Request not authorised')
        if authorised_agent != session.agent:
            raise NozomiError('Not authorised', HTTPStatusCode.NOT_AUTHORISED)
        assert authorised_agent == session.agent
        return response.broadcast_to(authorised_agent).serialise()
