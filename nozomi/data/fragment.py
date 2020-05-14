"""
Nozomi
Fragment Module
author: hugh@blinkybeach.com
"""
from nozomi.data.sql_conforming import SQLConforming
from nozomi.http.query_string import QueryString
from nozomi.ancillary.immutable import Immutable
from typing import TypeVar, Type, Optional

T = TypeVar('T', bound='Fragment')


class Fragment(SQLConforming):

    def __init__(self, fragment: str) -> None:
        assert isinstance(fragment, str)
        self._fragment = fragment
        return

    _wildcard_fragment = Immutable(lambda s: '%' + s._fragment + '%')
    sql_representation = Immutable(
        lambda s: s.adapt_string(s._wildcard_fragment)
    )
    value = Immutable(lambda s: s._fragment)

    @classmethod
    def from_arguments(
        cls: Type[T],
        arguments: QueryString,
        max_length: int = 64,
        min_length: int = 3,
        key: str = 'fragment'
    ) -> T:

        fragment = arguments.parse_string(
            key=key,
            max_length=max_length,
            min_length=min_length,
            allow_whitespace=True
        )

        return cls(fragment)

    @classmethod
    def optionally_from_arguments(
        cls: Type[T],
        arguments: QueryString,
        max_length: int = 64,
        min_length: int = 3,
        fallback_to_wildcard: bool = False,
        key='fragment'
    ) -> Optional[T]:

        fragment = arguments.optionally_parse_string(
            key=key,
            max_length=max_length,
            min_length=min_length,
            allow_whitespace=True
        )

        if fragment is None and fallback_to_wildcard is False:
            return None

        if fragment is None and fallback_to_wildcard is True:
            return cls.with_wildcard()

        return cls(fragment)

    @classmethod
    def with_wildcard(cls: Type[T]) -> T:
        return cls('%')
