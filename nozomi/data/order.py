"""
Nozomi
Order Module
author: hugh@blinkybeach.com
"""
from nozomi import SQLConforming, QueryString, BadRequest, Immutable
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
