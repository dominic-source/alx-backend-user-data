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
        return False

    def authorization_header(self, request=None) -> str:
        """Here is the authorisation header implemenation"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Verify current user of a url"""
        return None
