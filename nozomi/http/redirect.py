"""
Nozomi
Redirect Module
author: hugh@blinkybeach.com
"""
from typing import Optional, List
from nozomi.http.url_parameter import URLParameter
from nozomi.http.url_parameters import URLParameters


class Redirect(Exception):
    """
    An exception in program flow that requires the user to be redirected.
    """
    def __init__(
        self,
        destination: str,
        allow_next: bool = True,
        preserve_arguments: bool = True,
        extra_parameters: List[URLParameter] = list()
    ) -> None:

        assert isinstance(destination, str)
        assert isinstance(allow_next, bool)
        self._destination = destination
        self._allow_next = allow_next
        self._preserve_arguments = preserve_arguments
        self._base_parameters = extra_parameters

        return

    def destination(
        self,
        next_url: Optional[str] = None,
        query_string: bytes = b''
    ) -> str:
        """
        Return an application path to which a user should be
        redirected
        """
        destination = self._destination
        raw_parameters = self._base_parameters

        if next_url is not None and self._allow_next is True:
            assert isinstance(next_url, str)
            raw_parameters.append(URLParameter('then', next_url))

        if self._preserve_arguments is False:
            return destination

        raw_query_string = query_string.decode()
        elements = raw_query_string.split('&')
        for element in elements:
            if len(element) < 1:
                continue
            if element[0] == '?':
                element = element[1:]
            pieces = element.split('=')
            assert len(pieces) == 2
            raw_parameters.append(URLParameter(pieces[0], pieces[1]))
            continue

        parameters = URLParameters(raw_parameters)

        return parameters.add_to(destination)
