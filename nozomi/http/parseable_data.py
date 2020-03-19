"""
Nozomi
HTTP Request QueryString Module
Copyright Amatino Pty Ltd
"""
from collections.abc import Mapping
from typing import Optional, Dict, Any
from nozomi.errors.bad_request import BadRequest
import string
from decimal import Decimal


class ParseableData:
    """Generic parseable data, underlain by a mapping"""

    def __init__(self, raw: Mapping) -> None:
        self._raw = raw
        return

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

        if not isinstance(value, str):
            raise BadRequest('Value for key ' + key + ' must be string')

        return value

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

        if not isinstance(value, str):
            raise BadRequest('Value for key ' + key + ' must be string')

        if max_length is not None and len(value) > max_length:
            raise BadRequest(key + ' max length: ' + str(max_length))

        if min_length is not None and len(value) < min_length:
            raise BadRequest(key + ' min length: ' + str(min_length))

        if allow_whitespace is False:
            if True in [c in value for c in string.whitespace]:
                raise BadRequest('Whitespace not allowed')

        if filter_threats is True:
            if True in [f in value for f in ('UNION', 'union', 'SELECT',
                                             'select', 'DELETE', 'delete',
                                             'char(', 'CHAR(', 'CASE WHEN',
                                             'case when')]:
                raise BadRequest('Yikes!')

        return value

    def get(self, key: str) -> Optional[str]:
        value = self.optionally_parse_string(key)
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

        try:
            integer_value = int(value)
        except Exception:
            raise BadRequest(key + ' must be a string encoded integer')

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

        value = self.optionally_parse_int(key)
        if value is None:
            raise BadRequest('Missing ' + key + ' parameter')
        return value

    def optionally_parse_bool(
        self,
        key: str
    ) -> Optional[bool]:

        value = self.get(key)
        if value is None:
            return None

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
