"""
Nozomi
Configuration Module
author: hugh@blinkybeach.com
"""
from typing import List


class Configuration:
    """
    Abstract class defining an interface for a concrete class providing
    configuration to a Nozomi application
    """

    debug: bool = NotImplemented
    api_endpoint: str = NotImplemented

    session_seconds_to_live: int = NotImplemented
    session_api_key_name: str = NotImplemented
    session_cookie_key_name: str = NotImplemented
    session_id_name: str = NotImplemented

    standard_css_styles: List[str] = NotImplemented
    standard_js_classes: List[str] = NotImplemented
    standard_js_scripts: List[str] = NotImplemented