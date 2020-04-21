"""
Nozomi
HTTP Status Code Module
author: hugh@blinkybeach.com
"""
from enum import Enum


class HTTPStatusCode(Enum):
    """HTTP status codes per RFC 7231"""

    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303

    BAD_REQUEST = 400
    NOT_AUTHENTICATED = 401
    PAYMENT_REQUIRED = 402
    NOT_AUTHORISED = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    CONTENT_NOT_ACCEPTABLE = 406
    CONFLICT = 409
    PAYLOAD_TOO_LARGE = 413
    ALREADY_EXISTS = 422
    TOO_MANY_REQUESTS = 429

    INTERNAL_ERROR = 500
    NOT_IMPLEMENTED = 501
