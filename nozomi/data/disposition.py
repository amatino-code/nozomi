"""
Nozomi
Disposition Module
author: hugh@blinkybeach.com
"""
from nozomi.data.codable import Codable
from typing import TypeVar, Type, Any, Dict

T = TypeVar('T', bound='Disposition')


class Disposition(Codable):

    def __init__(
        self,
        sequence: int,
        count: int,
        limit: int,
        offset: int
    ) -> None:

        self._sequence = sequence
        self._count = count
        self._limit = limit
        self._offset = offset

        return

    def encode(self) -> Dict[str, int]:
        return {
            'sequence': self._sequence,
            'count': self._count,
            'limit': self._limit,
            'offset': self._offset
        }

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        return cls(
            sequence=data['sequence'],
            count=data['count'],
            limit=data['limit'],
            offset=data['offset']
        )
