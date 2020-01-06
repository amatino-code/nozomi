"""
Nozomi
NotAuthorised Error Module
author: hugh@blinkybeach.com
"""
from nozomi.errors.error import NozomiError
from nozomi.http.status_code import HTTPStatusCode


class NotFound(NozomiError):

    def __init__(
        self,
        client_description: str = 'A requested resource could not be found'
    ) -> None:

        super().__init__(
            client_description=client_description,
            http_status_code=HTTPStatusCode.NOT_FOUND
        )

        return
