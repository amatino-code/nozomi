"""
Nozomi
Secure View Module
author: hugh@blinkybeach.com
"""
from nozomi.rendering.view.base import BaseView
from nozomi.http.headers import Headers
from nozomi.http.query_string import QueryString
from nozomi.app.security.session import Session
from nozomi.security.perspective import Perspective
from nozomi.rendering.context import Context
from nozomi.security.considers_perspective import ConsidersPerspective
from typing import Optional, Set
from nozomi.security.agent import Agent


class SecureView(BaseView, ConsidersPerspective):
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

        session = Session.require_from_headers(
            headers=headers,
            configuration=self.configuration,
            signin_path=None
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
        context = self.compute_response(
            query=query,
            requesting_agent=session,
            context=context
        )

        return self.render(with_context=context)
