"""
Nozomi
Secure Resource Module
author: hugh@blinkybeach.com
"""
from nozomi.security.agent import Agent
from nozomi.resources.resource import Resource
from nozomi.http.query_string import QueryString
from nozomi.http.parseable_data import ParseableData
from nozomi.http.headers import Headers
from nozomi.data.encodable import Encodable
from typing import Optional, List, Union
from nozomi.data.datastore import Datastore
from nozomi.ancillary.immutable import Immutable
from nozomi.ancillary.configuration import Configuration


class OpenResource(Resource):
    """
    Abstract class defining an interface for for resources that do not require
    authentication, but that are aware of a requesting agent. For example, a web
    page that may be served differently depending on whether a user is logged in
    or not.
    """

    def __init__(
        self,
        datastore: Datastore,
        configuration: Configuration,
        requests_may_change_state: bool = False
    ) -> None:
        assert isinstance(datastore, Datastore)
        super().__init__(
            datastore=datastore,
            configuration=configuration
        )
        self._requests_may_change_state = requests_may_change_state
        return

    requests_may_change_state: bool = Immutable(
        lambda s: s._requests_may_change_state
    )

    def compute_response(
        self,
        request_data: Optional[ParseableData],
        request_arguments: Optional[QueryString],
        requesting_agent: Optional[Agent]
    ) -> Union[Encodable, List[Encodable]]:
        """
        Method returning an Encodable response
        """
        raise NotImplementedError

    def serve(
        self,
        request_data: Optional[ParseableData],
        request_arguments: Optional[QueryString],
        headers: Headers
    ) -> str:

        SessionImplementation = self.configuration.session_implementation

        session = SessionImplementation.from_headers(
            headers=headers,
            datastore=self.datastore,
            configuration=self.configuration,
            request_may_change_state=self.requests_may_change_state
        )
        response = self.compute_response(
            request_data,
            request_arguments,
            session
        )

        if isinstance(response, list):
            return Encodable.serialise_many(response)

        return response.serialise()
