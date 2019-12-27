"""
Nozomi
Secure View Module
author: hugh@blinkybeach.com
"""
from nozomi.rendering.view.base import BaseView
from nozomi.http.headers import Headers
from nozomi.http.query_string import QueryString
from nozomi.security.session import Session
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
        may_change_state: bool
    ) -> str:
        """
        Method returning the view as rendered for the supplied agent
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

        return self.compute_response(
            query=query,
            requesting_agent=session,
            context=context,
            may_change_state=may_change_state
        )
