#!/usr/bin/env python3
"""
Module defines a class SessionAuth that inherits from Auth.
"""
import uuid
from models.user import User
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
        session_id = str(uuid.uuid4())

        # Add user_id record
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns a user ID based on a SessionID"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value"""
        if request is None:
            return None

        # Get session id from cookie
        session_id = self.session_cookie(request)

        # Retrieve user id usinf session id
        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes the user session/logout"""
        if request is None:
            return False

        # Get session_id
        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        # Get user id using the session_id
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        # Delete session
        del user_id_by_session_id[session_id]

        return True
