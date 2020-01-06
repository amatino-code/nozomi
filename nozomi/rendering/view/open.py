"""
Nozomi
Open View Module
author: hugh@blinkybeach.com
"""
from nozomi.rendering.view.base import BaseView
from nozomi.http.headers import Headers
from nozomi.app.security.session import Session
from nozomi.rendering.context import Context
from typing import Optional
from nozomi.http.query_string import QueryString
from nozomi.security.agent import Agent


class OpenView(BaseView):
    """A view that supports optional authentication"""

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

        session = Session.from_headers(
            headers=headers,
            configuration=self.configuration
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
        context = self.compute_response(
            query=query,
            requesting_agent=session,
            context=context
        )

        return self.render(with_context=context)
