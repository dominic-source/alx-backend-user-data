#!/usr/bin/env python3

"""Module that inherits from sessionauth and expires it"""
from datetime import datetime, timedelta
import os
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Manage session expiry"""

    def __init__(self):
        """initialize expiration for auth"""
        time = os.environ.get("SESSION_DURATION")
        try:
            self.session_duration = int(time)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create session with expiry date"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        sec_dict = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = sec_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """user id using session id"""
        if session_id is None:
            return None
        data = self.user_id_by_session_id.get(session_id, None)
        if not data:
            return None
        if self.session_duration <= 0:
            return data.get("user_id")
        if not data.get("created_at", None):
            return None
        dtime = data.get("created_at") + timedelta(
                seconds=self.session_duration)
        current_dt = datetime.now()
        if dtime < current_dt:
            return None
        return data.get("user_id")
