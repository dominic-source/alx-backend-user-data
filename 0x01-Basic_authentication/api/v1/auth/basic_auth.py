#!/usr/bin/env python3

""" A Module that inherits from the authorisation
class
"""
from api.v1.auth.auth import Auth


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
