"""
Nozomi
Internal Resource Module
Copyright Amatino Pty Ltd
"""
from nozomi.data.datastore import Datastore
from nozomi.security.internal_key import InternalKey
from nozomi.resources.resource import Resource
from nozomi.http.query_string import QueryString
from typing import Optional, Tuple, Union, List
from nozomi.security.agent import Agent
from nozomi.security.broadcastable import Broadcastable
from nozomi.ancillary.configuration import Configuration
from nozomi.http.parseable_data import ParseableData
from nozomi.http.headers import Headers
from nozomi.security.forwarded_agent import ForwardedAgent
from nozomi.errors.not_authorised import NotAuthorised


class InternalResource(Resource):
    """
    Abstract class defining an interface for API requests that
    must only be served to applications inside a pre-shared key boundary.
    For example, requests from a web application server to an API.
    """

    def __init__(
        self,
        datastore: Datastore,
        configuration: Configuration
    ) -> None:

        super().__init__(
            datastore=datastore,
            configuration=configuration
        )

        if not isinstance(configuration.internal_psk, InternalKey):
            raise RuntimeError('Internal Resources require an InternalKey')

        return

    def compute_response(
        self,
        query: Optional[QueryString],
        unauthorised_agent: Agent,
        request_data: Optional[Union[ParseableData, List[ParseableData]]],
    ) -> Tuple[Union[Broadcastable, List[Broadcastable]], Agent]:
        # Method returning an encodable response, and an Agent authorised to
        # make the request.
        raise NotImplementedError

    def serve(
        self,
        request_data: Optional[ParseableData],
        request_arguments: Optional[QueryString],
        headers: Headers
    ) -> str:

        unauthorised_agent = ForwardedAgent.from_headers(
            internal_key=self.configuration.internal_psk,
            headers=headers,
            datastore=self.datastore,
            configuration=self.configuration
        )

        response, authorised_agent = self.compute_response(
            query=request_arguments,
            unauthorised_agent=unauthorised_agent,
            request_data=request_data
        )

        if not isinstance(authorised_agent, Agent):
            raise NotAuthorised

        if authorised_agent != unauthorised_agent:
            raise NotAuthorised
        assert authorised_agent == unauthorised_agent

        self.assert_read_available_to(
            unauthorised_agent=authorised_agent,
            broadcast_candidate=response
        )

        if isinstance(response, list):
            return Broadcastable.serialise_many(
                Broadcastable.broadcast_many_to(response, authorised_agent)
            )

        return response.broadcast_to(authorised_agent).serialise()
