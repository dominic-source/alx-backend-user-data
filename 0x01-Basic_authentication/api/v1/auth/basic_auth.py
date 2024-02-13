#!/usr/bin/env python3

""" A Module that inherits from the authorisation
class
"""
from models.user import User
from typing import TypeVar
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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """This method helps to extract user credentials"""
        if not decoded_base64_authorization_header:
            return None, None
        if type(decoded_base64_authorization_header) != str:
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        data = decoded_base64_authorization_header.split(':')
        return data[0], data[1]

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str
                                     ) -> TypeVar('User'):
        """create user object from credentials"""
        if not user_email or type(user_email) != str:
            return None
        if not user_pwd or type(user_pwd) != str:
            return None
        u = User.search({"email": user_email})
        if not u:
            return None
        if not u[0].is_valid_password(user_pwd):
            return None
        return u[0]
