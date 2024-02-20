#!/usr/bin/env python3

"""Manage authentication of users"""
from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError


def _hash_password(password: str) -> bytes:
    """hash password to hash and return bytes"""
    byte = password.encode('utf-8')
    # generating salt
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(byte, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register a user"""
        try:
            data = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            password_hashed = _hash_password(password)
            user = self._db.add_user(email, password_hashed)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate a user info"""
        try:
            data = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), data.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False
        except InvalidRequestError:
            return False
