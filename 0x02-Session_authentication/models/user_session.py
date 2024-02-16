#!/usr/bin/env python3

"""Manage sessions for database"""
from models.base import Base


class UserSession(Base):
    """Implement User session"""

    def __init__(self, *args: list, **kwargs: dict):
        """initialize the user session class"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get("user_id")
        self.session_id = kwargs.get("session_id")
