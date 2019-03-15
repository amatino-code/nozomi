"""
Nozomi
Decodable Protocol
Copyright Amatino Pty Ltd
"""
from json import loads
from typing import Any
from typing import TypeVar
from typing import Type

T = TypeVar('T', bound='Decodable')

_NOT_IMPLEMENTED_INFORMATION = """
Implemented a .decode(self, data: Any) method that returns an instance of your
concrete class, itself conforming to the Decodable protocol. The data parameter
will contain a composite of  str, int, float, dict & list types, i.e. types that
were natively deserialised from JavaScript Object Notation (JSON) format.
"""


class Decodable:
    """Abstract protocol defining an interface for decodable classes"""

    @classmethod
    def decode(self, data: Any) -> T:
        """Return an instance of the class conforming to Decodable"""
        raise NotImplementedError(_NOT_IMPLEMENTED_INFORMATION)

    @classmethod
    def deserialise(cls: Type[T], serial: str) -> T:
        """Return an instance of the class conforming to Decodable"""
        return cls.decode(loads(serial))
