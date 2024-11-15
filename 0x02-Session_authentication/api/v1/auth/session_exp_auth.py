#!/usr/bin/env python3
"""Module for class SessionExpAuth
"""
import os
from datetime import datetime
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Defines a class that adds an expiration date to SessionID"""
    def __ini__(self):
        """Initializes class"""
        self.session_duration = os.getenv('SESSION_DURATION', 0)

    def create_session(self, user_id=None):
        """Overrides parent method - Add created_atas value of
        SessionID.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Add session
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ """
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id:
            return None

        # Get session dictionary
        session_dict = self.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        if 'created_key' not in session_dict:
            return None

        # Check if the session has expired
        created_at = session_dict.get('created_at')
        if not isinstance(created_at, datetime):
            return None

        expiry_time = created_at + timedelta(
            seconds=self.session_duration)
        if expiry_time < datetime.now():
            return None

        returm session_dict.get('user_id')
