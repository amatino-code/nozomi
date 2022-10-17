"""
Nozomi
Publicly Identified Module
author: hugh@blinkybeach.com
"""
from nozomi.errors.not_found import NotFound
from nozomi.data.decodable import Decodable
from nozomi.data.datastore import Datastore
from nozomi.data.query import Query
from nozomi.data.named import Named
from typing import Type, TypeVar, Optional
from nozomi.http.parseable_data import ParseableData

Self = TypeVar('Self', bound='PubliclyIdentified')


class PubliclyIdentified(Decodable, Named):
    """
    Abstract class defining a protocol for classes that are publicly
    identified and consequently gain certain capabilities.
    """

    public_id: str = NotImplemented
    Q_RETRIEVE: Query = NotImplemented

    def __eq__(self, other) -> bool:
        if not type(self) == type(other):
            return False
        if self.public_id == other.public_id:
            return True
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.public_id)

    @classmethod
    def retrieve(
        Self: Type[Self],
        public_id: str,
        datastore: Datastore,
        in_transaction: bool = False
    ) -> Optional[Self]:

        result = Self.Q_RETRIEVE.execute(
            datastore=datastore,
            arguments={
                'public_id': public_id
            },
            atomic=(not in_transaction)
        )

        return Self.optionally_decode(result)

    @classmethod
    def retrieve_assertively(
        Self: Type[Self],
        public_id: str,
        datastore: Datastore,
        in_transaction: bool = False
    ) -> Optional[Self]:

        result = Self.retrieve(public_id, datastore, in_transaction)

        if result is None:
            raise NotFound('No {n} found with supplied public id'.format(
                n=Self.type_name if (
                    isinstance(Self.type_name, str)
                ) else 'object'
            ))

        return result

    @classmethod
    def from_request(
        Self: Type[Self],
        datastore: Datastore,
        data: ParseableData,
        key: str,
        in_transaction: bool = False
    ) -> Self:

        return Self.retrieve_assertively(
            public_id=data.parse_string(key),
            datastore=datastore,
            in_transaction=in_transaction
        )

    @classmethod
    def optionally_from_request(
        Self: Type[Self],
        datastore: Datastore,
        data: ParseableData,
        key: str,
        in_transaction: bool = False
    ) -> Optional[Self]:

        public_id = data.optionally_parse_string(key)

        return Self.retrieve_assertively(
            public_id=data.parse_string(key),
            datastore=datastore,
            in_transaction=in_transaction
        ) if public_id is not None else None
