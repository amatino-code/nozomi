"""
Nozomi
Secure View Module
author: hugh@blinkybeach.com
"""
from nozomi.rendering.view.open import OpenView
from nozomi.http.headers import Headers
from nozomi.http.query_string import QueryString
from nozomi.app.security.session import Session
from nozomi.security.perspective import Perspective
from nozomi.rendering.context import Context
from nozomi.security.considers_perspective import ConsidersPerspective
from typing import Optional, Set
from nozomi.security.agent import Agent
from nozomi.security.request_credentials import RequestCredentials


class SecureView(OpenView, ConsidersPerspective):
    """A view that requires authentication"""

    allowed_perspectives: Set[Perspective] = NotImplemented

    def compute_response(
        self,
        query: Optional[QueryString],
        requesting_agent: Agent,
        context: Context,
    ) -> Context:
        """
        Method returning the context as formed for the supplied request
        parameters
        """
        raise NotImplementedError

    def serve(
        self,
        headers: Headers,
        query: Optional[QueryString],
    ) -> str:

        session = self.session_implementation.require_from_headers(
            headers=headers,
            configuration=self.configuration,
            credentials=RequestCredentials.on_behalf_of_agent(
                agent=self.configuration.api_agent,
                configuration=self.configuration
            ),
            signin_path=None,
            request_may_change_state=self.requests_may_change_state
        )
        assert isinstance(session, Session)
        self.enforce_perspective(session)
        context = Context()
        context.add('agent', session.agent)
        context.add_javascript_constant('global_api_key', session.api_key)
        context.add_javascript_constant(
            'global_session_id',
            session.session_id
        )
        context.add_javascript_constant('requesting_agent_id', session.agent_id)
        context = self.compute_response(
            query=query,
            requesting_agent=session,
            context=context
        )

        return self.render(with_context=context)
