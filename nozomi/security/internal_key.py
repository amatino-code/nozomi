"""
Nozomi
Internal Key Module
Copyright Amatino Pty Ltd
"""
from nozomi.http.headers import Headers


class InternalKey:
    """
    Abstract protocol defining the behaviour of a key authenticating requests
    from internal applications.
    """
    HEADER_KEY = NotImplemented

    def matches_headers(self, headers: Headers) -> bool:
        """
        Return true if the supplied headers authenticate a request as
        coming from an internal application.
        """
        credential = headers.value_for(self.HEADER_KEY)
        if credential is None:
            return False
        return self.matches(credential)

    def matches(self, credential: str) -> bool:
        """
        Return true if the supplied credential authenticates a request
        as coming from an internal application.
        """
        raise NotImplementedError
