"""
Nozomi
View Module
author: hugh@blinkybeach.com
"""


class View:
    """
    An abstract class defining an interfaces for classes providing a web page
    view
    """

    def render(self) -> str:
        """Return a string rendering of this view"""
        raise NotImplementedError
