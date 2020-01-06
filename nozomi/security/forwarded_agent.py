"""
Nozomi
Forwarded Agent
author: hugh@blinkybeach.com
"""
from nozomi.security.standalone_agent import StandaloneAgent
from typing import TypeVar, Type
from nozomi.security.internal_key import InternalKey
from nozomi.http.headers import Headers
from nozomi.errors.not_authorised import NotAuthorised
from nozomi.errors.bad_request import BadRequest
from nozomi.data.datastore import Datastore

T = TypeVar('T', bound='ForwardedAgent')


class ForwardedAgent(StandaloneAgent):

    @classmethod
    def from_headers(
        cls: Type[T],
        internal_key: InternalKey,
        headers: Headers,
        datastore: Datastore
    ) -> T:

        assert isinstance(internal_key, InternalKey)
        assert isinstance(headers, Headers)

        if not internal_key.matches_headers(headers):
            raise NotAuthorised

        forwarded_agent_id = headers.get(cls.HEADER_KEY)
        if forwarded_agent_id is None:
            raise NotAuthorised

        try:
            agent_id = int(forwarded_agent_id)
        except ValueError:
            raise BadRequest('Bad forwarded agent ID')

        agent = cls.optionally_retrieve(
            agent_id=agent_id,
            datastore=datastore
        )

        if agent is None:
            raise NotAuthorised

        return agent
