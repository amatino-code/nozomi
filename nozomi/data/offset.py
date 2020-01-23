"""
Nozomi
Offset Module
author: hugh@blinkybeach.com
"""
from nozomi.http.query_string import QueryString
from nozomi.data.sql_conforming import SQLConforming
from nozomi.ancillary.immutable import Immutable
from typing import TypeVar, Type

T = TypeVar('T', bound='Offset')


class Offset(SQLConforming):

    def __init__(self, magnitude: int) -> None:
        assert isinstance(magnitude, int)
        self._magnitude = magnitude
        return

    sql_representation = Immutable(lambda s: s.adapt_integer(s._magnitude))
    magnitude = Immutable(lambda s: s._magnitude)

    @classmethod
    def from_arguments(
        cls: Type[T],
        arguments: QueryString,
        min_value: int = 0
    ) -> T:

        magnitude = arguments.parse_int(
            key='offset',
            min_value=min_value
        )

        return cls(magnitude)
