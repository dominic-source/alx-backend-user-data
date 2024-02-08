#!/usr/bin/env python3
"""This module is used to encrypt passwords to hash"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Convert a string password into an encrypted string"""
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed
