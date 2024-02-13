#!/usr/bin/env python3

"""This module contains the authentication class implmentation
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """The authentication class to authenticate users
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require that a user is authenticated"""

        if path is None:
            return True
        if not excluded_paths:
            return True
        if not path.endswith('/'):
            path = path + '/'
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Here is the authorisation header implemenation"""
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        else:
            return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """Verify current user of a url"""
        return None
