"""
Nozomi
Encodable Module
author: hugh@blinkybeach.com
"""
from json import dumps
from typing import Any, TypeVar, Type, List
from nozomi.data.format import Format
from nozomi.data.format import Constants as Formats
from nozomi.data.encoder import Encoder
from nozomi.data.abstract_encodable import AbstractEncodable

T = TypeVar('T', bound='Encodable')


class Encodable(AbstractEncodable):
    """Abstract protocol defining an interface for encodable classes"""

    def encode(self) -> Any:
        """Return a JSON-serialisable form of the object"""
        raise NotImplementedError

    def serialise(self, format: Format = Formats.JSON) -> str:
        """
        Return a string encoded representation of the object in the
        supplied format
        """
        assert isinstance(format, Format)
        if format != Formats.JSON:
            raise NotImplementedError(
                str(format.indexid) + ', ' + str(type(format))
            )
        return dumps(
            cls=Encoder,
            obj=self,
            separators=(',', ': '),
            sort_keys=True,
            indent=4
        )

    @classmethod
    def encode_many(cls: Type[T], data: List[T]) -> List[Any]:
        """Return a list of JSON-serialisable forms"""
        return [d.encode() for d in data]

    @classmethod
    def serialise_many(cls: Type[T], data: List[T]) -> str:
        """Return json serialised list data"""
        return dumps(
            cls=Encoder,
            obj=data,
            separators=(',', ': '),
            sort_keys=True,
            indent=4
        )
