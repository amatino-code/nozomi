"""
Nozomi
Open View Module
author: hugh@blinkybeach.com
"""
from nozomi.rendering.view.base import BaseView
from nozomi.http.headers import Headers
from nozomi.security.session import Session
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
        context: Context,
        may_change_state: bool
    ) -> str:
        """
        Method returning the view as rendered for the supplied agent, or no
        agent
        """
        raise NotImplementedError

    def serve(
        self,
        headers: Headers,
        query: Optional[QueryString],
        may_change_state: bool
    ) -> str:

        session = Session.require_from_headers(
            headers=headers,
            datastore=self.datastore,
            configuration=self.configuration,
            request_may_change_state=may_change_state
        )
        assert isinstance(session, Session)
        self.enforce_perspective(session)
        context = self.generate_context()
        context.add('agent', session.agent)
        context.add_javascript_constant('global_api_key', session.api_key)
        context.add_javascript_constant(
            'global_session_id',
            session.session_id
        )

        return super().render(headers=headers)
