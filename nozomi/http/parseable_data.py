"""
Nozomi
HTTP Request QueryString Module
Copyright Amatino Pty Ltd
"""
from collections.abc import Mapping
from typing import Optional, Dict, Any, List, TypeVar, Type, Generic
from enum import Enum
from nozomi.errors.bad_request import BadRequest
import string
from decimal import Decimal
from nozomi.ancillary.immutable import Immutable

T = TypeVar('T', bound='ParseableData')
_Number = TypeVar('_Number')


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
        allow_whitespace: bool = False,
        allowed_characters: Optional[str] = None,
        disallowed_characters: Optional[str] = None,
        inside: Optional[str] = None
    ) -> str:

        value = self.optionally_parse_string(
            key=key,
            max_length=max_length,
            min_length=min_length,
            allow_whitespace=allow_whitespace,
            allowed_characters=allowed_characters,
            disallowed_characters=disallowed_characters,
            inside=inside
        )

        if value is None:
            raise BadRequest('Missing value for key {i}'.format(
                i=key if inside is None else f'{inside}->{key}'
            ))

        return value

    def _validate_string(
        self,
        value: Any,
        key: str,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        allow_whitespace: bool = False,
        allowed_characters: Optional[str] = None,
        disallowed_characters: Optional[str] = None,
        inside: Optional[str] = None
    ) -> str:

        hint = key if inside is None else f'{inside}->{key}'

        if not isinstance(value, str):
            raise BadRequest(f'Value for key {hint} must be string')

        if max_length is not None and len(value) > max_length:
            raise BadRequest(f'{hint} max length: {max_length}')

        if min_length is not None and len(value) < min_length:
            raise BadRequest(f'{hint} min length: {min_length}')

        if allow_whitespace is False:
            if True in [c in value for c in string.whitespace]:
                raise BadRequest(f'Whitespace not allowed for key {hint}')

        if allowed_characters is not None:
            for character in value:
                if character not in allowed_characters:
                    raise BadRequest('Value for key {h} contains unacceptable \
characters. Acceptable characters: {a}'.format(
                        h=hint,
                        a=allowed_characters
                    ))
                continue
            pass
    
        if disallowed_characters is not None:
            for character in value:
                if character in disallowed_characters:
                    raise BadRequest('Value for key {h} contains unacceptable \
characters. Unacceptable characters: {d}'.format(
                        h=hint,
                        d=disallowed_characters
                    ))
                continue
            pass

        return value

    def optionally_parse_many_strings(
        self,
        key: str,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        allow_whitespace: bool = False,
        maximum_count: Optional[int] = None,
        delimiter: Optional[str] = None,
        allowed_characters: Optional[str] = None,
        disallowed_characters: Optional[str] = None,
        inside: Optional[str] = None
    ) -> Optional[List[str]]:

        values = self.parse_many_strings(
            key=key,
            max_length=max_length,
            min_length=min_length,
            allow_whitespace=allow_whitespace,
            maximum_count=maximum_count,
            minimum_count=0,
            delimiter=delimiter,
            allowed_characters=allowed_characters,
            disallowed_characters=disallowed_characters,
            inside=inside
        )

        return values if len(values) > 0 else None

    def parse_many_strings(
        self,
        key: str,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        allow_whitespace: bool = False,
        minimum_count: int = 0,
        maximum_count: Optional[int] = None,
        delimiter: Optional[str] = None,
        allowed_characters: Optional[str] = None,
        disallowed_characters: Optional[str] = None,
        inside: Optional[str] = None
    ) -> List[str]:

        hint = key if inside is None else f'{inside}->{key}'

        def derive_multikey_values() -> List[str]:
    
            if not hasattr(self._raw, 'getlist'):
                raise RuntimeError(self._MULTI_KEY_ERROR)

            return self._raw.getlist(key)

        def derive_delimited_values(delimiter: str) -> List[str]:

            raw_string = self.optionally_parse_string(key=key, inside=inside)

            return raw_string.split(delimiter) if raw_string else []

        def derive_values() -> List[str]:

            if delimiter is None:
                return derive_multikey_values()
            return derive_delimited_values(delimiter)

        values = derive_values()

        if len(values) < minimum_count:
            raise BadRequest('Supply at least {c} value(s) for key {k}'.format(
                c=str(minimum_count),
                k=hint
            ))

        if maximum_count is not None and len(values) > maximum_count:
            raise BadRequest('Supply at most {c} values for key {k}'.format(
                c=str(maximum_count),
                k=hint
            ))

        for value in values:
            self._validate_string(
                value=value,
                key=key,
                max_length=max_length,
                min_length=min_length,
                allow_whitespace=allow_whitespace,
                allowed_characters=allowed_characters,
                disallowed_characters=disallowed_characters
            )
            continue

        return values

    def optionally_parse_string(
        self,
        key: str,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        allow_whitespace: bool = False,
        allowed_characters: Optional[str] = None,
        disallowed_characters: Optional[str] = None,
        inside: Optional[str] = None
    ) -> Optional[str]:

        value = self.get(key)

        if value is None:
            return None

        return self._validate_string(
            value=value,
            key=key,
            max_length=max_length,
            min_length=min_length,
            allow_whitespace=allow_whitespace,
            allowed_characters=allowed_characters,
            disallowed_characters=disallowed_characters,
            inside=inside
        )

    def get(
        self,
        key: str,
        of_type: Optional[Type] = None,
        type_name: Optional[str] = None,
        inside: Optional[str] = None
    ) -> Optional[Any]:

        hint = key if inside is None else f'{inside}->{key}'

        if key not in self._raw.keys():
            return None

        value = self._raw[key]

        if value is None:
            return None

        if of_type is not None and not isinstance(value, of_type):
            if of_type == int and isinstance(value, str):
                try:
                    int_value = int(value)
                    return int_value
                except Exception:
                    pass
            if type_name is None:
                raise BadRequest(f'Value for key {hint} has incorrect type')
            raise BadRequest('Value for key {k} must be {t}'.format(
                k=hint,
                t=type_name
            ))

        return value

    def require(
        self,
        key: str,
        of_type: Optional[Type] = None,
        type_name: Optional[str] = None,
        inside: Optional[str] = None
    ) -> Any:

        value = self.get(key, of_type, type_name=type_name, inside=inside)
        if value is None:
            raise BadRequest('Missing value for key {k}'.format(
                k=key if inside is None else f'{inside}->{key}'
            ))

        return value

    def optionally_parse_enum(
        self,
        key: str,
        enum_type: Type[Enum],
        type_name: str,
        inside: Optional[str] = None
    ) -> Optional[Enum]:

        value = self.get(key, of_type=type([v.value for v in enum_type][0]))
        if value is None:
            return None

        try:
            result = enum_type(value)
        except ValueError:
            raise BadRequest('Bad {t} value for enumeration at key {k}. Accept\
able values: {v}'.format(
                t=type_name,
                k=key if inside is None else f'{inside}->{key}',
                v=str([v.value for v in enum_type])
                )
            )

        return result

    def parse_enum(
        self,
        key: str,
        enum_type: Type[Enum],
        type_name: str,
        inside: Optional[str] = None
    ) -> Optional[Enum]:

        value = self.optionally_parse_enum(
            key=key,
            enum_type=enum_type,
            type_name=type_name
        )

        if value is not None:
            return value

        raise BadRequest('Missing {k} parameter'.format(
            k=key if inside is None else f'{inside}->{key}'
        ))

    def optionally_parse_int(
        self,
        key: str,
        max_value: Optional[int] = None,
        min_value: Optional[int] = None,
        inside: Optional[str] = None
    ) -> Optional[int]:

        value = self.get(key)
        if value is None:
            return None

        return self._validate_integer(
            key=key,
            candidate=value,
            max_value=max_value,
            min_value=min_value,
            inside=inside
        )

    def _validate_integer(
        self,
        key: str,
        candidate: Any,
        max_value: Optional[int] = None,
        min_value: Optional[int] = None,
        inside: Optional[str] = None
    ) -> int:

        if isinstance(candidate, bool):
            raise BadRequest(
                '{k} must be integer or string encoded integer'.format(
                    k=key if inside is None else f'{inside}->{key}'
                )
            )

        try:
            integer_value = int(candidate)
        except Exception:
            raise BadRequest(
                '{k} must be integer or string encoded integer'.format(
                    k=key if inside is None else f'{inside}->{key}'
                )
            )

        return self._constrain_number(
            key=key,
            number=integer_value,
            max_value=max_value,
            min_value=min_value,
            inside=inside
        )

    def parse_int(
        self,
        key: str,
        max_value: Optional[int] = None,
        min_value: Optional[int] = None,
        inside: Optional[str] = None
    ) -> int:

        value = self.optionally_parse_int(
            key,
            max_value=max_value,
            min_value=min_value,
            inside=inside
        )
        if value is None:
            raise BadRequest('Missing {k} parameter'.format(
                k=key if inside is None else f'{inside}->{key}'
            ))

        return value

    def parse_many_ints(
        self,
        key: str,
        max_value: Optional[int] = None,
        min_value: Optional[int] = None,
        minimum_count: int = 0,
        maximum_count: Optional[int] = None,
        inside: Optional[str] = None
    ) -> List[int]:

        if not hasattr(self._raw, 'getlist'):
            raise RuntimeError(self._MULTI_KEY_ERROR)

        values = self._raw.getlist(key)

        if len(values) < minimum_count:
            raise BadRequest('{k} must provide at least {n} integers'.format(
                k=key if inside is None else f'{inside}->{key}',
                n=str(minimum_count)
            ))

        if maximum_count is not None and len(values) > maximum_count:
            raise BadRequest('{k} must provide no more than {n} \
integers'.format(
                k=key if inside is None else f'{inside}->{key}',
                n=str(maximum_count)
            ))

        validated: List[int] = list()
        for value in values:
            validated.append(self._validate_integer(
                key=key,
                candidate=value,
                max_value=max_value,
                min_value=min_value,
                inside=inside
            ))

        return validated

    def optionally_parse_bool(
        self,
        key: str,
        fallback_to: Optional[bool] = None,
        inside: Optional[str] = None
    ) -> Optional[bool]:

        value = self.get(key)
        if value is None:
            return fallback_to

        if isinstance(value, bool):
            return value

        if value == 'true':
            return True
        if value == 'false':
            return False

        hint = key if inside is None else f'{inside}->{key}'

        raise BadRequest(f'{hint} must be "true" or "false"')

    def parse_bool(
        self,
        key: str,
        inside: Optional[str] = None
    ) -> bool:

        value = self.optionally_parse_bool(key)
        if value is None:
            raise BadRequest('{k} parameter missing'.format(
                k=key if inside is None else f'{inside}->{key}'
            ))

        return value

    def optionally_parse_decimal(
        self,
        key: str,
        max_value: Optional[Decimal] = None,
        min_value: Optional[Decimal] = None,
        inside: Optional[str] = None
    ) -> Optional[Decimal]:

        value = self._raw.get(key)
        if value is None:
            return None

        try:
            decimal_value = Decimal(str(value))
        except Exception:
            raise BadRequest('{k} must be a string encoded decimal'.format(
                k=key if inside is None else f'{inside}->{key}'
            ))

        return self._constrain_number(
            key=key,
            number=decimal_value,
            max_value=max_value,
            min_value=min_value,
            inside=inside
        )

    def parse_decimal(
        self,
        key: str,
        max_value: Optional[Decimal] = None,
        min_value: Optional[Decimal] = None,
        inside: Optional[str] = None
    ) -> Decimal:

        decimal = self.optionally_parse_decimal(
            key=key,
            max_value=max_value,
            min_value=min_value
        )

        if decimal is None:
            raise BadRequest('Missing string encoded decimal for key `{k}`\
'.format(k=key if inside is None else f'{inside}->{key}'))

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

    def optionally_parse_enum_array(
        self,
        key: str,
        enum_type: Type[Enum],
        type_name: str,
        min_elements: Optional[int] = None,
        max_elements: Optional[int] = None,
        delimiter: Optional[str] = None,
        inside: Optional[str] = None
    ) -> Optional[List[Enum]]:

        def check() -> Optional[Any]:
            if delimiter is None:
                return self.get(
                    key=key,
                    of_type=list, type_name='array',
                    inside=inside
                )
            return self.optionally_parse_string(key)

        if check() is None:
            return None
        
        return self.parse_enum_array(
            key=key,
            enum_type=enum_type,
            type_name=type_name,
            min_elements=min_elements,
            max_elements=max_elements,
            delimiter=delimiter,
            inside=inside
        )

    def parse_enum_array(
        self,
        key: str,
        enum_type: Type[Enum],
        type_name: str,
        min_elements: Optional[int] = None,
        max_elements: Optional[int] = None,
        delimiter: Optional[str] = None,
        inside: Optional[str] = None
    ) -> List[Enum]:

        def derive_array() -> List[Any]:
            if delimiter is None:
                return self.require(
                    key,
                    of_type=list,
                    type_name='array',
                    inside=inside
                )
            return self.parse_many_strings(
                key=key,
                delimiter=delimiter,
                inside=inside
            )

        array = derive_array()

        if min_elements is not None:
            if len(array) < min_elements:
                raise BadRequest('{k} array minimum elements is {i}'.format(
                    k=key if inside is None else f'{inside}->{key}',
                    i=str(min_elements)
                ))
            pass

        if len(array) < 1:
            return array

        if max_elements is not None:
            if len(array) > max_elements:
                raise BadRequest('{k} array maximum length is {i}'.format(
                    k=key if inside is None else f'{inside}->{key}',
                    i=str(max_elements)
                ))
            pass

        valid_enum_values = [c.value for c in enum_type]
        enum_base_type = type(valid_enum_values[0])
        supplied_type = type(array[0])
        map_string_to_int = False

        # Allow string-encoded integers to satisfy integer type requirements
        if enum_base_type == int and supplied_type == str:
            map_string_to_int = True
            valid_enum_values = [str(v) for v in valid_enum_values]

        for item in array:
            if item not in valid_enum_values:
                raise BadRequest('Bad {t} value for enumeration at key {k}. Ac\
ceptable values: {v}'.format(
                        t=type_name,
                        k=key if inside is None else f'{inside}->{key}',
                        v=str(valid_enum_values)
                    )
                )
            continue

        if map_string_to_int is True:
            return [enum_type(int(i)) for i in array]
        return [enum_type(i) for i in array]

    def parse_string_array(
        self,
        key: str,
        max_length: Optional[int] = None,
        min_length: Optional[int] = None,
        allow_whitespace: bool = False,
        allowed_characters: Optional[str] = None,
        disallowed_characters: Optional[str] = None,
        min_elements: Optional[int] = None,
        max_elements: Optional[int] = None,
        inside: Optional[str] = None
    ) -> List[str]:

        array = self.require(
            key=key,
            of_type=list,
            type_name='array',
            inside=inside
        )

        if min_elements is not None:
            if len(array) < min_elements:
                raise BadRequest('{k} array minimum elements is {i}'.format(
                    k=key if inside is None else f'{inside}->{key}',
                    i=str(min_elements)
                ))

        if len(array) < 1:
            return array

        if max_elements is not None:
            if len(array) < min_elements:
                raise BadRequest('{k} array maximum length is {i}'.format(
                    k=key if inside is None else f'{inside}->{key}',
                    i=str(max_elements)
                ))

        for item in array:
            self._validate_string(
                value=item,
                key=key,
                max_length=max_length,
                min_length=min_length,
                allow_whitespace=allow_whitespace,
                allowed_characters=allowed_characters,
                disallowed_characters=disallowed_characters,
                inside=inside
            )
            continue

        return array

    def _constrain_number(
        self,
        key: str,
        number: _Number,
        max_value: Optional[_Number],
        min_value: Optional[_Number],
        inside: Optional[str] = None
    ) -> _Number:

        if min_value is not None and number < min_value:
            raise BadRequest('{k} below mininum value: {m}'.format(
                k=key if inside is None else f'{inside}->{key}',
                m=str(min_value)
            ))

        if max_value is not None and number > max_value:
            raise BadRequest('{k} above maximum value: {m}'.format(
                k=key if inside is None else f'{inside}->{key}',
                m=str(max_value)
            ))

        return number

    def _validate_float(
        self,
        key: str,
        candidate: Any,
        max_value: Optional[float] = None,
        min_value: Optional[float] = None,
        inside: Optional[str] = None
    ) -> float:

        if isinstance(candidate, bool):
            raise BadRequest('{k} must be float or string encoded float\
'.format(
                k=key if inside is None else f'{inside}->{key}'
            ))

        try:
            float_value = float(candidate)
        except Exception:
            raise BadRequest('{k} must be float or string encoded float\
'.format(
                k=key if inside is None else f'{inside}->{key}'
            ))

        return self._constrain_number(
            key=key,
            number=float_value,
            max_value=max_value,
            min_value=min_value,
            inside=inside
        )

    def optionally_parse_float(
        self,
        key: str,
        max_value: Optional[float] = None,
        min_value: Optional[float] = None,
        inside: Optional[str] = None
    ) -> Optional[float]:

        value = self._raw.get(key)
        if value is None:
            return None

        return self._validate_float(
            key=key,
            candidate=value,
            max_value=max_value,
            min_value=min_value,
            inside=inside
        )

    def parse_float(
        self,
        key: str,
        max_value: Optional[float] = None,
        min_value: Optional[float] = None,
        inside: Optional[str] = None
    ) -> float:

        value = self.optionally_parse_float(
            key=key,
            max_value=max_value,
            min_value=min_value,
            inside=inside
        )

        if value is None:
            raise BadRequest('Missing {k} parameter'.format(
                k=key if inside is None else f'{inside}->{key}'
            ))

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
