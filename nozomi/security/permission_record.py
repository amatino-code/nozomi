"""
Nozomi
Permission Record Module
Copyright Amatino Pty Ltd
"""
from nozomi.data.encodable import Encodable
from nozomi.data.decodable import Decodable
from nozomi.security.agent import Agent
from typing import TypeVar
from typing import Any
from typing import Type
from typing import List

T = TypeVar('T', bound='PermissionRecord')


class PermissionRecord(Encodable, Decodable):
    """A record of ownership and read / write permissions for an object"""

    def __init__(
        self,
        owned_by: str,
        readable_by: List[str],
        writable_by: List[str],
        administered_by: List[str]
    ) -> None:

        assert isinstance(owned_by, int)
        assert isinstance(readable_by, list)
        assert isinstance(writable_by, list)
        assert isinstance(administered_by, list)
        assert False not in [isinstance(r, str) for r in readable_by]
        assert False not in [isinstance(w, str) for w in writable_by]
        assert False not in [isinstance(a, str) for a in administered_by]

        self._owned_by = owned_by
        self._readable_by = readable_by
        self._writable_by = writable_by
        self._administered_by = administered_by

        return

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            data['owned_by'],
            data['readable_by'],
            data['writable_by'],
            data['administered_by']
        )

    def encode(self) -> Any:
        return {
            'owned_by': self._owned_by,
            'readable_by': self._readable_by,
            'writable_by': self._writable_by,
            'administered_by': self._administered_by
        }

    def records_admin_permission_for(self, agent: Agent) -> bool:
        """Return True if admin permissions are recorded for an Agent"""
        if (self.records_ownership_by(agent)):
            return True
        if agent.agent_id in self._administered_by:
            return True
        return False

    def records_write_permission_for(self, agent: Agent) -> bool:
        """Return True if write permissions are recorded for an Agent"""
        if self.records_ownership_by(agent):
            return True
        return agent.agent_id in self._writable_by

    def records_read_permission_for(self, agent: Agent) -> bool:
        """Return True of read permissions are recorded for an Agent"""
        if self.records_ownership_by(agent):
            return True
        return agent.agent_id in self._readable_by

    def records_ownership_by(self, agent: Agent) -> bool:
        """Return True if ownership is recorded for an Agent"""
        if agent.agent_id == self._owned_by:
            return True
        return False
