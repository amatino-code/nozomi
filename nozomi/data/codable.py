"""
Nozomi
Codable Data Module
author: hugh@blinkybeach.com
"""
import sys
from nozomi import Encodable, Decodable
from typing import TypeVar, Type, Any, Union, Dict, Optional, List
from typing import Callable
from enum import Enum
from decimal import Decimal

T = TypeVar('T', bound='Codable')
K = TypeVar('K', bound='CodableType')

Object = Dict[str, K]
Array = List[K]
CodableType = Union[T, int, Object, Array, str, float, Enum, Decimal]

_QUANTUM_TYPES = (int, str, float, dict, list, bool)


class CodingDefinition:

    def __init__(
        self,
        codable_type: Type[CodableType],
        optional: bool = False,
        array: bool = False,
        default_value_generator: Optional[Callable[[], CodableType]] = None
    ) -> None:

        if (
                codable_type not in _QUANTUM_TYPES
                and Enum not in codable_type.__bases__
                and codable_type != Decimal
                and Codable not in codable_type.__bases__
        ):
            raise TypeError('CodingDefinition  requires that the `codable_type\
` parameter be one of either (int, str, float, bool, dict, list, Enum, Decimal\
) or be a custom type that inherits from Nozomi.Codable. The supplied codable_\
type {x} does not appear to meet these requirements.\
'.format(x=str(codable_type)))

        default_value: Optional[CodableType] = None
        if default_value_generator is not None:
            default_value = default_value_generator()

        self._codable_type = codable_type
        self._optional = optional
        self._array = array
        self._default_value = default_value

        return

    def decode(self, data: Any) -> Any:

        try:

            if data is None:
                if self._optional is True:
                    if self._default_value is not None:
                        return self._default_value
                    return None
                raise RuntimeError('Unexpectedly null data when decoding')

            if Enum in self._codable_type.__bases__:
                if self._array is True:
                    return [self._codable_type(d) for d in data]
                return self._codable_type(data)

            if self._codable_type == Decimal:
                return Decimal(data)

            if Codable not in self._codable_type.__bases__:
                return data

            if self._array is True and self._optional is True:
                return self._codable_type.optionally_decode_many(
                    data=data,
                    default_to_empty_list=True
                )
            if self._array is True:
                return self._codable_type.decode_many(data)
            if self._optional is True:
                return self._codable_type.optionally_decode(data)
            return self._codable_type.decode(data)
        except Exception:
            if '--debug' in sys.argv or '--test' in sys.argv:
                print('Failed to decode {t}:'.format(
                    t=str(self._codable_type)
                ))
                print(data)
            raise


class Codable(Encodable, Decodable):

    coding_map: Dict[str, CodingDefinition] = NotImplemented

    def encode(self):

        def recurse(
            attribute: Optional[CodableType]
        ) -> Optional[CodableType]:

            if attribute is None:
                return None

            if type(attribute) in (int, str, float, bool):
                return attribute

            if isinstance(attribute, Enum):
                return recurse(attribute.value)

            if isinstance(attribute, Decimal):
                return str(attribute)

            if isinstance(attribute, dict):
                return {k: recurse(attribute[k]) for k in attribute}

            if isinstance(attribute, list):
                return [recurse(a) for a in attribute]

            if Codable in type(attribute).__bases__:
                return attribute.encode()

            raise RuntimeError('Unexpected type: ' + str(attribute))

        return {k: recurse(self.__dict__['_' + k]) for k in self.coding_map}

    @classmethod
    def decode(cls: Type[T], data: Any) -> T:
        c = cls.coding_map
        return cls(**{k: c[k].decode(data[k]) for k in c})
