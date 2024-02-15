#!/usr/bin/env python3

"""This module is set to help us learn about sessions
and how it works
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Implement a session management system"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create a session for our authentication"""
        if not user_id:
            return None
        if type(user_id) != str:
            return None
        s_id = str(uuid.uuid4())
        SessionAuth.user_id_by_session_id[s_id] = user_id
        return s_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """return user_id of a sesssion"""
        if session_id is None:
            return None
        if type(session_id) != str:
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)
