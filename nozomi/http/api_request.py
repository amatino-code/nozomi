"""
Nozomi
API Request Module
author: hugh@blinkybeach.com
"""
from nozomi.http.method import HTTPMethod
from nozomi.ancillary.configuration import Configuration
from nozomi.ancillary.immutable import Immutable
from nozomi.http.url_parameters import URLParameters
from urllib.request import Request
from urllib.request import urlopen
from typing import Any, Optional, TypeVar
from nozomi.security.agent import Agent
from urllib.request import HTTPError
import json

T = TypeVar('T', bound='ApiRequest')


class ApiRequest:
    """A request to a Nozomi-compliant API via HTTP"""

    def __init__(
        self,
        path: str,
        method: HTTPMethod,
        configuration: Configuration,
        on_behalf_of_agent: Agent,
        data: Optional[Any] = None,
        url_parameters: Optional[URLParameters] = None
    ) -> None:

        assert isinstance(on_behalf_of_agent, Agent)

        url = configuration.api_endpoint + path
        if url_parameters is not None:
            url = url_parameters.add_to(url)

        headers = {
            configuration.internal_psk_header: configuration.api_psk,
            configuration.forwarded_agent_header: on_behalf_of_agent.agent_id
        }

        if data is not None:
            data = json.dumps(data).encode('utf-8')
            headers['content-type'] = 'application/json'

        request = Request(
            url,
            method=method.value,
            data=data,
            headers=headers
        )

        try:
            response = urlopen(request).read()
        except HTTPError as error:
            if error.code == 404:
                self._response_data = None
                return
            raise

        self._response_data = json.loads(response)

        return

    response_data = Immutable(lambda s: s._response_data)
