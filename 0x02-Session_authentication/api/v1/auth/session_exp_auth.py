#!/usr/bin/env python3
"""Module for class SessionExpAuth
"""
import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Defines a class that adds an expiration date to SessionID"""
    def __init__(self):
        """Initializes class"""
        try:
            duration = int(os.getenv('SESSION_DURATION'))
        except ValueError:
            duration = 0

        self.session_duration = duration

    def create_session(self, user_id=None):
        """Overrides parent method - Add created_atas value of
        SessionID.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        # Replace session id value with new dict
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Before searching for  user_id using session_id check for
           Expiration of that session user.
           Return:
                   None:     If session expired
                   user_id:  If session is active and user  is valid
        """
        if session_id is None:
            return None

        if session_id not in self.user_id_by_session_id:
            return None

        # Get session dictionary
        session_dict = self.user_id_by_session_id[session_id]

        # Session logic does not apply to this
        if self.session_duration <= 0:
            return session_dict.get('user_id')

        if 'created_at' not in session_dict:
            return None

        # Check if the session has exspired
        created_at = session_dict.get('created_at')
        if not isinstance(created_at, datetime):
            return None

        expiry_time = created_at + timedelta(
            seconds=self.session_duration)
        if expiry_time < datetime.now():
            return None

        return session_dict.get('user_id')
