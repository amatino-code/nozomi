"""
Nozomi
Configuration Module
author: hugh@blinkybeach.com
"""
from nozomi.ancillary.database_credentials import DatabaseCredentials
from typing import Optional, List
from nozomi.security.internal_key import InternalKey
from nozomi.security.agent import Agent
from nozomi.ancillary.immutable import Immutable


class Configuration:
    """
    Abstract class defining an interface for a concrete class providing
    configuration to a Nozomi application
    """

    debug: bool = NotImplemented
    api_endpoint: str = NotImplemented
    public_api_endpoint: str = Immutable(
        lambda s: s.api_endpoint
    )

    # Sessions

    session_seconds_to_live: int = NotImplemented
    session_api_key_name: str = NotImplemented
    session_cookie_key_name: str = NotImplemented
    session_id_name: str = NotImplemented
    session_flag_cookie_name: str = NotImplemented

    internal_psk_header: str = NotImplemented
    internal_psk: Optional[InternalKey] = NotImplemented

    forwarded_agent_header: str = NotImplemented

    standard_css_styles: List[str] = NotImplemented
    standard_js_classes: List[str] = NotImplemented
    standard_js_scripts: List[str] = NotImplemented

    database_credentials: DatabaseCredentials = NotImplemented

    api_agent: Agent = NotImplemented

    # CORS
    local_origin: str = NotImplemented
    restricted_origin: str = NotImplemented
    disable_cors_restriction: bool = NotImplemented

    # Other
    server_name: str = NotImplemented
    boundary_ip_header: str = NotImplemented
