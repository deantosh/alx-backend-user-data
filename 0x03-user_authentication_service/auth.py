#!/usr/bin/env python3
"""
Module defines methods used in user authentication system.
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Encrypts user password"""

    # Convert to binary
    b_password = password.encode("UTF-8")

    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(b_password, salt)

    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
          Create a new user:
            - If user exists: raise ValueError
            - If user not found: create and add user to database
          Return: new user.
        """
        # Handle: if user exists
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {user.email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)

            # Create a new user
            user = self._db.add_user(email, hashed_password)

            return user
