"""
Nozomi
Open View Module
author: hugh@blinkybeach.com
"""
from nozomi.rendering.view.base import BaseView
from nozomi.http.headers import Headers
from nozomi.rendering.context import Context
from nozomi.rendering.open_graph import OpenGraph
from nozomi.ancillary.configuration import Configuration
from nozomi.security.abstract_session import AbstractSession
from typing import List, Dict, Optional, Any, Type
from nozomi.http.query_string import QueryString
from nozomi.security.agent import Agent
from nozomi.security.request_credentials import RequestCredentials


class OpenView(BaseView):
    """A view that supports optional authentication"""

    session_implementation: Type[AbstractSession] = NotImplemented
    requests_may_change_state: bool = NotImplemented

    def __init__(
        self,
        configuration: Configuration,
        template: str,
        title: str,
        description: str,
        key_words: List[str],
        styles: List[str],
        scripts: List[str],
        classes: List[str],
        open_graph: Optional[OpenGraph] = None,
        static_variables: Optional[Dict[str, Any]] = None,
        static_js_constants: Optional[Dict[str, Any]] = None
    ) -> None:

        assert isinstance(self.session_implementation, type)
        assert isinstance(self.requests_may_change_state, bool)

        super().__init__(
            configuration=configuration,
            template=template,
            title=title,
            description=description,
            key_words=key_words,
            styles=styles,
            scripts=scripts,
            classes=classes,
            open_graph=open_graph,
            static_variables=static_variables,
            static_js_constants=static_js_constants
        )

        return

    def compute_response(
        self,
        query: Optional[QueryString],
        requesting_agent: Optional[Agent],
        context: Context
    ) -> Context:
        """
        Method returning the context as formed for the supplied request
        parameters
        """
        raise NotImplementedError

    def serve(
        self,
        headers: Headers,
        query: Optional[QueryString]
    ) -> str:

        session = self.session_implementation.from_headers(
            headers=headers,
            configuration=self.configuration,
            credentials=RequestCredentials.on_behalf_of_agent(
                agent=self.configuration.api_agent,
                configuration=self.configuration
            ),
            request_may_change_state=self.requests_may_change_state
        )

        context = Context()
        context.add('agent', session.agent if session is not None else None)
        context.add_javascript_constant(
            'global_api_key',
            session.api_key if session is not None else None
        )
        context.add_javascript_constant(
            'global_session_id',
            session.session_id if session is not None else None
        )
        context.add_javascript_constant(
            'requesting_agent_id',
            session.agent_id if session is not None else None
        )
        context = self.compute_response(
            query=query,
            requesting_agent=session,
            context=context
        )

        return self.render(with_context=context)
