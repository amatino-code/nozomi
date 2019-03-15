"""
Nozomi
Broadcastable Module
Copyright Amatino Pty Ltd
"""
from nozomi.security.agent import Agent
from nozomi.transmission.encodable import Encodable
from typing import Any

BROADCAST_TYPE_ERROR = """
The default Broadcastable.Broadcast type may only accept data of type int, str,
float, list or dict. You supplied {datatype}.
"""


class Broadcastable(Encodable):
    """
    Abstract class defining an interface for concrete classes who may be asked
    to provide a broadcastable representation of themselves. For example,
    an object may contain internal fields that should not be visible outside
    the application. A broadcastable representation of the object would
    strip those fields and return an Encodable version of its data, suitable
    for return to an application.

    Broadcastable provides a 
    """
    _VALID_TYPES = {str, int, dict, list, float}

    def broadcast_to(self, agent: Agent) -> Encodable:
        """
        Return an encodable form of this object suitable for broadcast
        to the supplied Agent.
        """
        raise NotImplementedError

    class Broadcast(Encodable):
        def __init__(self, encoded_data: Any) -> None:
            _type = type(encoded_data)
            if _type not in Broadcastable._VALID_TYPES:
                raise TypeError(BROADCAST_TYPE_ERROR.format(_type=str(_type)))

            self._data = encoded_data
            return

        def encode(self) -> Any:
            return self._data
