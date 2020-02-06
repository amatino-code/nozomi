"""
Nozomi
Forwarded Agent
author: hugh@blinkybeach.com
"""
from nozomi.security.standalone_agent import StandaloneAgent
from typing import TypeVar, Type, Optional
from nozomi.security.internal_key import InternalKey
from nozomi.http.headers import Headers
from nozomi.errors.not_authorised import NotAuthorised
from nozomi.data.datastore import Datastore
from nozomi.ancillary.configuration import Configuration

T = TypeVar('T', bound='ForwardedAgent')


class ForwardedAgent(StandaloneAgent):

    @classmethod
    def from_headers(
        cls: Type[T],
        internal_key: InternalKey,
        headers: Headers,
        datastore: Datastore,
        configuration: Configuration
    ) -> T:

        assert isinstance(internal_key, InternalKey)
        assert isinstance(headers, Headers)

        if not internal_key.matches_headers(headers):
            raise NotAuthorised

        forwarded_agent_id = headers.value_for(
            configuration.forwarded_agent_header
        )
        if forwarded_agent_id is None:
            raise NotAuthorised

        agent = cls.optionally_retrieve(
            public_id=forwarded_agent_id,
            datastore=datastore
        )

        if agent is None:
            raise NotAuthorised

        return agent

    @classmethod
    def optionally_from_headers(
        cls: Type[T],
        internal_key: InternalKey,
        headers: Headers,
        datastore: Datastore,
        configuration: Configuration
    ) -> Optional[T]:

        assert isinstance(internal_key, InternalKey)
        assert isinstance(headers, Headers)

        if not internal_key.matches_headers(headers):
            return None

        forwarded_agent_id = headers.value_for(
            configuration.forwarded_agent_header
        )
        if forwarded_agent_id is None:
            return None

        agent = cls.optionally_retrieve(
            public_id=forwarded_agent_id,
            datastore=datastore
        )

        if agent is None:
            raise None

        return agent
