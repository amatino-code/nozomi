"""
Nozomi
Database Credentials Module
author: hugh@blinkybeach.com
"""
from nozomi.ancillary.immutable import Immutable
from nozomi.data.decodable import Decodable
import json
from typing import TypeVar, Type, Dict

T = TypeVar('T', bound='DatabaseCredentials')


class DatabaseCredentials(Decodable):
    """Stores and disburses database connection credentials"""

    def __init__(
        self,
        host: str,
        secret: str,
        database_name: str,
        user: str,
        port: str
    ) -> None:

        credentials = (host, secret, database_name, user)
        assert False not in [isinstance(c, str) for c in credentials]
        self._host = host
        self._secret = secret
        self._database_name = database_name
        self._user = user
        self._port = port

        return

    dsn_string: str = Immutable(lambda s: s._form_dsn_string())

    def _form_dsn_string(self) -> str:
        """Return a psycopg2 compatible 'dsn' string"""
        dsn = 'host=' + self._host
        dsn += ' dbname=' + self._database_name
        dsn += ' user=' + self._user
        dsn += ' port=' + self._port
        dsn += ' password=' + self._secret
        return dsn

    def apply_to_template(
        self,
        template: str,
        other_arguments: dict = {}
    ) -> str:
        """
        Return a string after applying secret, host, user, and dbname parameters
        to a template string
        """
        return template.format(
            secret=self._secret,
            user=self._user,
            host=self._host,
            dbname=self._database_name,
            **other_arguments
        )

    @classmethod
    def from_json(cls: Type[T], json_data: str) -> T:
        assert isinstance(json_data, str)
        return cls.decode(json.loads(json_data))

    @classmethod
    def decode(cls: Type[T], data: Dict) -> T:
        if not isinstance(data, dict):
            raise TypeError('data must be of type dict')

        try:
            credentials = cls(
                host=data['host'],
                secret=data['secret'],
                database_name=data['database_name'],
                user=data['user'],
                port=data['port']
            )
        except KeyError as error:
            raise ValueError('Missing key ' + str(error.args[0]))

        return credentials
