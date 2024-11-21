#!/usr/bin/env python3
"""
Module defines methods used in user authentication system.
"""
import bcrypt
import uuid
from db import DB
from user import User
from typing import Optional
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Encrypts user password"""

    # Convert to binary
    b_password = password.encode("UTF-8")

    # Generate salt and hash password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(b_password, salt)

    return hashed_password


def _generate_uuid() -> str:
    """'Generate user id"""
    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """Check if a valid user is logging in"""

        # Check if user email is valid
        try:
            user = self._db.find_user_by(email=email)

            # Convert password to bytes
            b_password = password.encode("UTF-8")

            result = bcrypt.checkpw(b_password, user.hashed_password)

            return result
        except NoResultFound:
            return False

    def create_session(self, email: str) -> Optional[str]:
        """Creates a user session id"""

        try:
            # Get user if exists
            user = self._db.find_user_by(email=email)

            # Create session id
            session_id = _generate_uuid()

            # Update current user session id
            self._db.update_user(user.id, session_id=session_id)

            return session_id

        except NoResultFound:
            return None

    def get_user_from_session_id(
            self, session_id: str) -> Optional[User]:
        """Retrieves user based on his/her session id"""

        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
