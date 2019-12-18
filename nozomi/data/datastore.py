"""
Nozomi
Datastore Module
Copyright Amatino Pty Ltd
"""
import psycopg2
from nozomi.ancillary.database_credentials import DatabaseCredentials
from typing import Type, TypeVar, Any, Optional, Dict
from nozomi.data.sql_conforming import AnySQLConforming

T = TypeVar('T', bound='Datastore')


class Datastore:
    """An abstraction of a persistent data storage layer"""

    def __init__(
        self,
        credentials: DatabaseCredentials
    ) -> None:

        assert isinstance(credentials, DatabaseCredentials)
        self._credentials = credentials
        self._connection = psycopg2.connect(dsn=credentials.dsn_string)
        self._cursor = self._connection.cursor()

        return

    def _refresh(self) -> None:
        """Connect or re-connect the underlying database connection"""
        self._connection = psycopg2.connect(dsn=self._credentials.dsn_string)
        self._cursor = self._connection.cursor()
        return

    def execute(
        self,
        query: str,
        arguments: Optional[Dict[str, AnySQLConforming]] = None,
        atomic=False
    ) -> Optional[Any]:
        """
        Execute a supplied SQL query string with the supplied arguments. The
        Datastore will attempt to recover from broken connections in flight. If
        the query is denoted as atomic. That is, it is not transaction
        dependent.
        """
        try:
            self._cursor.execute(query, arguments)
        except (
            psycopg2.OperationalError,
            psycopg2.InterfaceError,
            psycopg2.InternalError
        ):
            if atomic is False:
                raise
            try:
                self._connection.close()
                self._cursor.close()
            except Exception:
                pass
            self._refresh()
            self._cursor.execute(query, arguments)
        if self._cursor.description is None:
            return None
        result = self._cursor.fetchone()
        if result is None:
            return None
        if atomic is True:
            self.commit()
        return result[0]

    def close(self) -> None:
        self._cursor.close()
        self._connection.close()
        return

    def commit(self) -> None:
        self._cursor.execute('commit')
        return

    def mogrify(self, query: str, arguments: Optional[Dict[str, Any]]) -> str:
        """Return a string compiled query"""
        return self._cursor.mogrify(query, arguments).decode()

    def rollback(self) -> None:
        """Roll back the current transaction"""
        self._cursor.execute('rollback')

    def start_transaction(self) -> None:
        """Start a database transaction"""
        self._cursor.execute('start transaction')

    @classmethod
    def from_config(cls: Type[T], configuration: Any):
        credentials = configuration.database_credentials
        return cls(credentials)
