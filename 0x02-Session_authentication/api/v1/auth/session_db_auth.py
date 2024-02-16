#!/usr/bin/env python3

"""Implement the session database"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


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
        if type(session_id) != str:
            return None
        data = UserSession.search({"session_id": session_id})
        if not data:
            return None
        if self.session_duration <= 0:
            return data[0].user_id
        if not data[0].created_at:
            return None
        fromtime = data[0].created_at
        dtime = fromtime + timedelta(
                seconds=self.session_duration)
        current_dt = datetime.now()
        if dtime < current_dt:
            return None
        return data[0].user_id

    def destroy_session(self, request=None):
        """destroy a user session"""
        cookie_name = os.environ.get("SESSION_NAME")
        if not request:
            return False
        session_id = request.cookies.get(cookie_name)
        if session_id is None:
            return False
        user = UserSession.search({"session_id": session_id})
        if not user:
            return False
        d_user = user.remove()
        return True
