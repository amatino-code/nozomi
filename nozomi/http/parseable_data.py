"""
Nozomi
HTTP Request QueryString Module
Copyright Amatino Pty Ltd
"""
from collections.abc import Mapping
from typing import Optional, Dict, Any, List, TypeVar, Type
from nozomi.errors.bad_request import BadRequest
import string
from decimal import Decimal
from nozomi.ancillary.immutable import Immutable

T = TypeVar('T', bound='ParseableData')


class ParseableData:
    """Generic parseable data, underlain by a mapping"""

    _MULTI_KEY_ERROR = 'Data structure underpinning ParseableData does \
not provide a .getlist() method for multiple values per key'

    def __init__(self, raw: Mapping) -> None:
        if raw is None:
            raise BadRequest('Expected a key/value object')
        self._raw = raw
        return

    raw = Immutable(lambda s: s._raw)

    def parse_string(
        self,
        key: str,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        filter_threats: bool = True,
        allow_whitespace: bool = False
    ) -> str:

        value = self.optionally_parse_string(
            key=key,
            max_length=max_length,
            min_length=min_length,
            filter_threats=filter_threats,
            allow_whitespace=allow_whitespace
        )

        if value is None:
            raise BadRequest('Missing value for key ' + key)

        return value

    def _validate_string(
        self,
        value: Any,
        key: str,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        filter_threats: bool = True,
        allow_whitespace: bool = False
    ) -> str:

        if not isinstance(value, str):
            raise BadRequest('Value for key ' + key + ' must be string')

        if max_length is not None and len(value) > max_length:
            raise BadRequest(key + ' max length: ' + str(max_length))

        if min_length is not None and len(value) < min_length:
            raise BadRequest(key + ' min length: ' + str(min_length))

        if allow_whitespace is False:
            if True in [c in value for c in string.whitespace]:
                raise BadRequest('Whitespace not allowed')

        #if filter_threats is True:
        #    if True in [f in value for f in ()]:
        #        raise BadRequest('Yikes!')

        return value

    def parse_many_strings(
        self,
        key: str,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        filter_threats: bool = True,
        allow_whitespace: bool = False,
        minimum_count: int = 0,
        maximum_count: Optional[int] = None
    ) -> List[str]:

        if not hasattr(self._raw, 'getlist'):
            raise RuntimeError(self._MULTI_KEY_ERROR)

        values = self._raw.getlist(key)

        if len(values) < minimum_count:
            raise BadRequest('Supply at least {c} value for key {k}'.format(
                c=str(minimum_count),
                k=key
            ))

        if maximum_count is not None and len(values) > maximum_count:
            raise BadRequest('Supply less than {c} values for key {k}'.format(
                c=str(maximum_count),
                k=key
            ))

        for value in values:
            self._validate_string(
                value=value,
                key=key,
                max_length=max_length,
                min_length=min_length,
                filter_threats=filter_threats,
                allow_whitespace=allow_whitespace
            )

        return values

    def optionally_parse_string(
        self,
        key: str,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        filter_threats: bool = True,
        allow_whitespace: bool = False
    ) -> Optional[str]:

        value = self._raw.get(key)

        if value is None:
            return None

        return self._validate_string(
            value=value,
            key=key,
            max_length=max_length,
            min_length=min_length,
            filter_threats=filter_threats,
            allow_whitespace=allow_whitespace
        )

    def get(self, key: str, of_type: Optional[Type] = None) -> Optional[Any]:
        if key not in self._raw.keys():
            return None

        value = self._raw[key]
        if of_type is not None and not isinstance(value, of_type):
            raise BadRequest('Value for key ' + key + ' has incorrect type')

        return value

    def require(
        self,
        key: str,
        of_type: Optional[Type] = None
    ) -> Any:

        value = self.get(key, of_type)
        if value is None:
            raise BadRequest('Missing value for key ' + key)

        return value

    def optionally_parse_int(
        self,
        key: str,
        max_value: Optional[int] = None,
        min_value: Optional[int] = None
    ) -> Optional[int]:

        assert isinstance(key, str)

        value = self._raw.get(key)
        if value is None:
            return None

        return self._validate_integer(
            key=key,
            candidate=value,
            max_value=max_value,
            min_value=min_value
        )

    def _validate_integer(
        self,
        key: str,
        candidate: Any,
        max_value: Optional[int] = None,
        min_value: Optional[int] = None
    ) -> int:

        if isinstance(candidate, bool):
            raise BadRequest(key + ' must be integer or string encoded integer')

        try:
            integer_value = int(candidate)
        except Exception:
            raise BadRequest(key + ' must be integer or string encoded integer')

        if min_value is not None and integer_value < min_value:
            raise BadRequest(key + ' below mininum value: ' + str(min_value))

        if max_value is not None and integer_value > max_value:
            raise BadRequest(key + ' above maximum value: ' + str(max_value))

        return integer_value

    def parse_int(
        self,
        key: str,
        max_value: Optional[int] = None,
        min_value: Optional[int] = None
    ) -> int:

        value = self.optionally_parse_int(
            key,
            max_value=max_value,
            min_value=min_value
        )
        if value is None:
            raise BadRequest('Missing ' + key + ' parameter')

        return value

    def parse_many_ints(
        self,
        key: str,
        max_value: Optional[int] = None,
        min_value: Optional[int] = None,
        minimum_count: int = 0,
        maximum_count: Optional[int] = None
    ) -> List[int]:

        if not hasattr(self._raw, 'getlist'):
            raise RuntimeError(self._MULTI_KEY_ERROR)

        values = self._raw.getlist(key)

        if len(values) < minimum_count:
            raise BadRequest('{k} must provide at least {n} integers'.format(
                k=key,
                n=str(minimum_count)
            ))

        if maximum_count is not None and len(values) > maximum_count:
            raise BadRequest('{k} must provide no more than {n} \
integers'.format(
                k=key,
                n=str(maximum_count)
            ))

        validated: List[int] = list()
        for value in values:
            validated.append(self._validate_integer(
                key=key,
                candidate=value,
                max_value=max_value,
                min_value=min_value
            ))

        return validated

    def optionally_parse_bool(
        self,
        key: str
    ) -> Optional[bool]:

        value = self.get(key)
        if value is None:
            return None

        if isinstance(value, bool):
            return value

        if value == 'true':
            return True
        if value == 'false':
            return False

        raise BadRequest(key + ' must be "true" or "false"')

    def parse_bool(
        self,
        key: str
    ) -> bool:

        value = self.optionally_parse_bool(key)
        if value is None:
            raise BadRequest(key + ' parameter missing')

        return value

    def optionally_parse_decimal(
        self,
        key: str,
        max_value: Optional[Decimal] = None,
        min_value: Optional[Decimal] = None
    ) -> Optional[Decimal]:

        value = self._raw.get(key)
        if value is None:
            return None

        try:
            decimal_value = Decimal(value)
        except Exception:
            raise BadRequest(key + ' must be a string encoded decimal')

        if min_value is not None and decimal_value < min_value:
            raise BadRequest(key + ' below mininum value: ' + str(min_value))

        if max_value is not None and decimal_value > max_value:
            raise BadRequest(key + ' above maximum value: ' + str(max_value))

        return decimal_value

    def parse_decimal(
        self,
        key: str,
        max_value: Optional[Decimal] = None,
        min_value: Optional[Decimal] = None
    ) -> Decimal:

        decimal = self.optionally_parse_decimal(
            key=key,
            max_value=max_value,
            min_value=min_value
        )

        if decimal is None:
            raise BadRequest(key + ' missing string encoded decimal for key \
`{k}`'.format(k=key))

        return decimal

    def parse_integer_array(
        self,
        key: str
    ) -> List[int]:

        value = self.raw.get(key)
        error = key + ' must be an array of integers'
        if not isinstance(value, list):
            raise BadRequest(error)
        if False in [isinstance(v, int) for v in value]:
            raise BadRequest(error)
        return value

    def __iter__(self):
        return ParseableData.Iterator(self._raw)

    class Iterator:
        """An iterator for iterating through LedgerRows in a Ledger"""

        def __init__(self, pairs: Dict[str, Any]) -> None:
            self._index = 0
            self._pairs = pairs
            self._keys = [k for k in pairs.keys()]
            return

        def __next__(self) -> str:
            if self._index >= len(self._keys):
                raise StopIteration
            item = self._keys[self._index]
            self._index += 1
            return item

    def __len__(self):
        return len(self._keys)

    def __getitem__(self, key):
        return self._raw[key]

    def __str__(self) -> str:
        return str(self._raw)

    @classmethod
    def many(cls: Type[T], data: List[Any]) -> List[T]:
        if not isinstance(data, list):
            raise BadRequest('Expected array/sequence of data in body')
        return [cls(d) for d in data]
