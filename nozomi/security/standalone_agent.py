"""
Nozomi
Standalone Agent Protocol Module
author: hugh@blinkybeach.com
"""
from nozomi.security.agent import Agent
from nozomi.data.datastore import Datastore
from nozomi.data.query import Query
from nozomi.ancillary.immutable import Immutable
from nozomi.errors.not_found import NotFound
from typing import Type, TypeVar, Any, Optional

T = TypeVar('T', bound='StandaloneAgent')


class StandaloneAgent(Agent):
    """
    Astract protocol degning an interface for classes who may be granted
    access to read or write objects. At the MVP stage, this is most likely
    to be Humans.
    """
    _Q_RETRIEVE = Query.optionally_from_file(
        'queries/secrity/agents/retrieve.sql'
    )

    def __init__(
        self,
        agent_id: int
    ) -> None:

        assert isinstance(agent_id, int)
        self._agent_id = agent_id

        return

    agent_id = Immutable(lambda s: s._agent_id)
    indexid = Immutable(lambda s: s._agent_id)

    Q_RETRIEVE = Immutable(lambda s: Query.require(s._Q_RETRIEVE, 'Standalone\
Agent retrieval'))

    def __eq__(self, other) -> bool:
        if not isinstance(other.agent_id, int):
            return False
        if not isinstance(self.agent_id, int):
            return False
        return other.agent_id == self.agent_id

    @classmethod
    def retrieve(cls: Type[T], agent_id: int, datastore: Datastore) -> T:
        """Retrieve an Agent with the supplied ID, or raise an exception"""
        agent = cls.optionally_retrieve(agent_id, datastore)
        if agent is None:
            raise NotFound
        return agent

    @classmethod
    def optionally_retrieve(
        cls: Type[T],
        agent_id: int,
        datastore: Datastore
    ) -> Optional[T]:
        """Retrieve an Agent with the supplied ID, or None"""
        result = cls.Q_RETRIEVE.execute(datastore, {'agent_id': agent_id})
        if result is None:
            return None
        return cls.decode(result)

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        """Return an Agent decoded from serialised data"""
        return cls(agent_id=data['agent_id'])
