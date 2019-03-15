"""
Nozomi
Encodable Module
Copyright Amatino Pty Ltd
"""
from json import dumps
from typing import Any

_NOT_IMPLEMENTED_INFORMATION = """
Implement a .encode() method that returns a str, int, float, dict, list, or
any composite thereof. I.e any type that may be natively serialised to
JavaScript Object Notation (JSON) format.
"""


class Encodable:
    """Abstract protocol defining an interface for encodable classes"""

    def encode(self) -> Any:
        """Return a JSON-serialisable form of the object"""
        raise NotImplementedError(_NOT_IMPLEMENTED_INFORMATION)

    def serialise(self) -> str:
        """Return a JSON string representation of the object"""
        return dumps(self.encode())
