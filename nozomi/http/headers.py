"""
Nozomi
HTTP Headers Module
Copyright Amatino Pty Ltd
"""
from typing import Optional


class Headers:
    """
    Abstract class defining an interface for a class that represents HTTP
    Headers
    """

    def value_for(self, key: str) -> Optional[str]:
        """
        Return the value of a supplied header key, or None if no value
        exists for that key.
        """
        raise NotImplementedError
