"""
Nozomi
Style Module
Author: hugh@blinkybeach.com
"""
from nozomi.rendering.render_dependency import RenderDependency


class Style(RenderDependency):
    """
    A cascading style sheet (.css) file required by a template
    """
    _PATH = 'styles/'
    _EXTENSION = '.css'
    _NAME = 'Style'

    def __init__(self, script_name) -> None:

        super().__init__(
            script_name=script_name,
            path=self._PATH,
            extension=self._EXTENSION,
            name=self._NAME
        )
        return
