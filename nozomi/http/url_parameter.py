"""
Nozomi
URL Parameter Module
author: hugh@blinkybeach.com
"""
from typing import Any, TypeVar, List
from nozomi.ancillary.immutable import Immutable


Self = TypeVar('Self', bound='URLParameter')


class URLParameter:

    """A single URL parameter, e.g. beep=boop"""

    def __init__(
        self,
        key: str,
        value: Any
    ) -> None:

        if not isinstance(key, str):
            raise TypeError('key must be of type `str`')

        if isinstance(value, bool):
            value = str(value).lower()

        try:
            str(value)
        except:
            raise TypeError(
                'value must be of type that may be coerced to `str'
            )

        self._key = key
        self._value = value

        return

    @staticmethod
    def remove_targets_with(
        key: str,
        parameters: List[Self]
    ) -> List[Self]:

        retained_targets: List[URLParameter] = []
        for target in parameters:
            if target._key == key:
                continue
            retained_targets.append(target)
            continue
            
        return retained_targets

    key: str = Immutable(lambda s: s._key)

    def __str__(self) -> str:
        return self._key + '=' + str(self._value)


QueryParameter = URLParameter
