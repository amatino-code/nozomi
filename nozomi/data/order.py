"""
Nozomi
Order Module
author: hugh@blinkybeach.com
"""
from nozomi.http.query_string import QueryString
from nozomi.errors.bad_request import BadRequest
from nozomi.ancillary.immutable import Immutable
from nozomi.data.sql_conforming import SQLConforming
from typing import TypeVar, Type

T = TypeVar('T', bound='Order')


class Order(SQLConforming):

    def __init__(
        self,
        ascending: bool
    ) -> None:

        self._ascending = ascending

        return

    sql_representation = Immutable(
        lambda s: b'asc' if s._ascending else b'desc'
    )
    ascending: bool = Immutable(lambda s: s._ascending)
    descending: bool = Immutable(lambda s: not s._ascending)

    def __str__(self) -> str:
        return 'asc' if self._ascending else 'desc'

    @classmethod
    def from_arguments(
        cls: Type[T],
        arguments: QueryString,
        default_to_descending: bool = False
    ) -> T:

        order = arguments.optionally_parse_string(
            key='order',
            max_length=32
        )

        if order is None:
            if default_to_descending is False:
                raise BadRequest(
                    'Supply order=[ascending|descending] parameter'
                )
            return cls(True)

        if order.lower() == 'ascending':
            return cls(True)

        if order.lower() == 'descending':
            return cls(False)

        raise BadRequest('Acceptable `order` values: ascending, descending')
