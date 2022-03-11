"""
Nozomi
HTTP Request QueryString Module
Copyright Amatino Pty Ltd
"""
from nozomi.http.parseable_data import ParseableData
from typing import TypeVar, Type, Any, Optional
from urllib.parse import unquote


class QueryString(ParseableData):
    """A URL QueryString, aka URL parameters"""

    def get(
        self,
        key: str,
        of_type: Optional[Type] = None,
        type_name: Optional[str] = None
    ) -> Optional[Any]:

        value = super().get(
            key=key,
            of_type=of_type,
            type_name=type_name
        )

        if isinstance(value, str):
            return unquote(value)
        
        return value
