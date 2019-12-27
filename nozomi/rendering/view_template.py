"""
Nozomi
View Template Module
author: hugh@blinkybeach.com
"""
from typing import Optional
from nozomi.rendering.context import Context


class ViewTemplate:

    template: str = NotImplemented

    def render(self, context: Optional[Context]) -> str:
        """
        Execute stage 2 render, returning a string HTML page for provision to
        a client.
        """
        if context is None:
            return self.template.render(Context().context)
        return self.template.render(**context.context)
