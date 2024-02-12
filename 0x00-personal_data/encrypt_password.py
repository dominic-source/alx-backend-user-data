#!/usr/bin/env python3
"""This module is used to encrypt passwords to hash"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Convert a string password into an encrypted string"""
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Verify if password matches the hashed password"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
