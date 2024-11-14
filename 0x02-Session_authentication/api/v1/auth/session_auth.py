#!/usr/bin/env python3
"""
Module defines a class SessionAuth that inherits from Auth.
"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Defines a session authentication system"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a SessionID for a user_id"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None

        # Generate SessionID
        session_id = uuid.uuid4()

        # Add user_id record
        self.user_id_by_session_id[session_id] = user_id

        return session_id
