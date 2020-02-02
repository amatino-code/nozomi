"""
Nozomi
Abstract API Session Module
author: hugh@blinkybeach.com
"""
from nozomi.data.decodable import Decodable
from nozomi.security.agent import Agent
from nozomi.ancillary.immutable import Immutable
from nozomi.security.perspective import Perspective
from nozomi.http.headers import Headers
from typing import TypeVar, Type, Any, Optional

T = TypeVar('T', bound='AbstractSession')


class AbstractSession(Decodable, Agent):

    session_id: str = NotImplemented
    session_key: str = NotImplemented
    agent: Agent = NotImplemented
    perspective: Perspective = NotImplemented
    api_key: str = NotImplemented

    agent_id = Immutable(lambda s: s._agent.agent_id)

    @classmethod
    def from_headers(
        cls: Type[T],
        headers: Headers,
        configuration: Any,
        request_may_change_state: bool = True
    ) -> Optional[T]:

        raise NotImplementedError

    @classmethod
    def require_from_headers(
        cls: Type[T],
        headers: Headers,
        configuration: Any,
        request_may_change_state: bool = True
    ) -> T:

        raise NotImplementedError