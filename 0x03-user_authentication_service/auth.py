#!/usr/bin/env python3
"""
Module defines methods used in user authentication system.
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """Encrypts user password"""

    # Convert to binary
    b_password = password.encode("UTF-8")

    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(b_password, salt)

    return hashed_password
