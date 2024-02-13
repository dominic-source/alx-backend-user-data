#!/usr/bin/env python3

""" A Module that inherits from the authorisation
class
"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """The basic auth class"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extract base authorization header"""
        if not authorization_header:
            return None
        if type(authorization_header) != str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        token = authorization_header.split(' ')[1]
        return token

    def decode_base64_authorization_header(
                                           self,
                                           base64_authorization_header: str
                                           ) -> str:
        """decode authorisation header"""
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) != str:
            return None

        try:
            encoded = base64_authorization_header.encode("utf-8")
            data = base64.b64decode(encoded)
        except Exception:
            return None
        return data.decode('utf-8')
