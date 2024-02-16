#!/usr/bin/env python3

"""Implement the session database"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session database authentication system"""

    def create_session(self, user_id=None):
        """Create and store new instatnce of usersession"""
        s_id = super().create_session(user_id)
        if not s_id:
            return None
        user = UserSession(user_id=user_id, session_id=s_id)
        user.save()
        return s_id

    def user_id_for_session_id(self, session_id=None):
        """get user id for session id"""
        if session_id is None:
            return None
        user = UserSession.search({"session_id": session_id})
        if not user:
            return None
        return user[0].user_id

    def destroy_session(self, request=None):
        """destroy a user session"""
        cookie_name = os.environ.get("SESSION_NAME")
        if not request:
            False
        session_id = request.cookies.get(cookie_name)
        if session_id is None:
            return False
        user = UserSession.search({"session_id": session_id})
        if not user:
            return False
        d_user = user.remove()
        return True
