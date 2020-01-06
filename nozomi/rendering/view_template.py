"""
Nozomi
View Template Module
author: hugh@blinkybeach.com
"""
from typing import Optional
from jinja2 import Environment, FileSystemLoader
from nozomi.rendering.context import Context

LOADER = FileSystemLoader('templates')
STAGE_1_ENVIRONMENT = Environment(  # Static context
    loader=LOADER,
    block_start_string='{&',
    block_end_string='&}',
    variable_start_string='+{',
    variable_end_string='}+'
)
STAGE_2_ENVIRONMENT = Environment(
    loader=LOADER,
    block_start_string='{%',
    block_end_string='%}',
    variable_start_string='{{',
    variable_end_string='}}'
)  # Dynamic context


class ViewTemplate:
    """
    An HTML template to be populated by runtime View data. Template rendering
    occurs in two stages. Stage 1 renders data known at application start, such
    as CSS files. Stage 2 renders data known at request time, such as a logged
    in user name . The two are separated by different Jinja2 templating markers.
    """

    def __init__(self, template_filename: str, static_context: Context) -> None:
        with open('templates/' + template_filename) as template_file:
            template_string = template_file.read()
        self._stage_1_render = STAGE_1_ENVIRONMENT.from_string(
            template_string
        ).render(static_context.context)
        self._template = STAGE_2_ENVIRONMENT.from_string(self._stage_1_render)
        return

    def render(self, context: Optional[Context]) -> str:
        """
        Execute stage 2 render, returning a string HTML page for provision to
        a client.
        """
        if context is None:
            return self._template.render(Context().context)
        return self._template.render(**context.context)
