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
