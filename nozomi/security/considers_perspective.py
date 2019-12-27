"""
Nozomi
ConsidersPerspective Module
author: hugh@blinkybeach.com
"""
from nozomi.security.perspective import Perspective
from nozomi.security.session import Session
from nozomi.http.redirect import Redirect
from nozomi.rendering.context import Context
from typing import Set


class ConsidersPerspective:
    """Abstract class defining a protocol for views conscious of perspective"""

    allowed_perspectives: Set[Perspective] = NotImplemented

    def enforce_perspective(self, session: Session) -> None:
        """Return None if the supplied Session perspective is acceptable"""
        if not isinstance(self.allowed_perspectives, set):
            raise NotImplementedError('Implement .allowed_perspectives')
        if (
                session.perspective not in self.allowed_perspectives
                and session.perspective != Perspective.ADMINISTRATOR
        ):
            raise Redirect(destination=session.dashboard_path, allow_next=False)
        return

    def register_perspective_flags(
        self,
        context: Context,
        session: Session
    ) -> Context:

        if session.perspective == Perspective.BUSINESS:
            context.add('business_perspective', True)
        else:
            context.add('business_perspective', False)

        if session.perspective == Perspective.SUPPLIER:
            context.add('supplier_perspective', True)
        else:
            context.add('supplier_perspective', False)

        if session.perspective == Perspective.ADMINISTRATOR:
            context.add('admin_perspective', True)
        else:
            context.add('admin_perspective', False)

        return context
