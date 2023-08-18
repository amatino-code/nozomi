"""
Nozomi
HTTPMethod Module
Copyright Amatino Pty Ltd
"""
from enum import Enum
from typing import TypeVar, Type, Any

Self = TypeVar('Self', bound='HTTPMethod')


class HTTPMethod(Enum):

    GET = 'GET'
    POST = 'POST'
    DELETE = 'DELETE'
    PUT = 'PUT'
    PATCH = 'PATCH'
    OPTIONS = 'OPTIONS'
    HEAD = 'HEAD'
    CONNECT = 'CONNECT'
    TRACE = 'TRACE'

    UNKNOWN = 'UNKNOWN'

    @classmethod
    def _missing_(Self: Type[Self], value: Any) -> Self:
        return Self.UNKNOWN
