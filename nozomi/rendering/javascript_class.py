"""
Nozomi Web
JavaScript Class Module
Author: hugh@blinkybeach.com
"""
from nozomi.rendering.render_dependency import RenderDependency


class JavaScriptClass(RenderDependency):
    """
    A javascript (.js) file required by a template
    """
    _PATH = 'javascript/classes/'
    _EXTENSION = '.js'
    _NAME = 'JavaScriptClass'

    def __init__(self, script_name) -> None:

        super().__init__(
            script_name=script_name,
            path=self._PATH,
            extension=self._EXTENSION,
            name=self._NAME
        )
        return
