"""
Nozomi
Broadcastable Module
Copyright Amatino Pty Ltd
"""


class Agent:
    """
    Astract protocol defining an interface for classes who may be granted
    access to read or write objects.
    """
    agent_id: str = NotImplemented

    def __eq__(self, other) -> bool:
        if not isinstance(other.agent_id, int):
            return False
        if not isinstance(self.agent_id, int):
            return False
        if not isinstance(other, Agent):
            return False
        return other.agent_id == self.agent_id
