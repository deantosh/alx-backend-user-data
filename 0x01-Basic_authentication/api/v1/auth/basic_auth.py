#!/usr/bin/env python3
"""
Module defines a class BasicAuth that inherits from Auth class.
"""
import base64
from typing import TypeVar
from models.user import User
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Empty class - not implemented"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Returns the Base64 part of the authorization header
           for a Basic Authentication.
        """
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None

        # Retrieve header value
        return authorization_header.split(' ', 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Returns the decode value of a Base64 string
           base64_authorization_header
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None

        try:
            # Decode base64 string
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_str = decoded_bytes.decode('utf-8')
            return decoded_str
        except (base64.binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Returns the user email and password from the Base64 decode value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ':' not in decoded_base64_authorization_header:
            return (None, None)

        # Extract user email and password from string
        email, password = decoded_base64_authorization_header.split(':', 1)

        return (email, password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns the User instance based on his email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Find if user exists
        users = User.search({'email': user_email})

        # If no user with user_email exists
        if not users:
            return None

        # Get the first user
        user = users[0]

        # check is provided password is correct
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the user instance for a request"""
        # Get the Authorization header from request
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # Extract base64_part from authorization header
        base64_part = self.extract_base64_authorization_header(auth_header)
        if base64_part is None:
            return None

        # Decode base64_part string
        base64_str = self.decode_base64_authorization_header(base64_part)
        if base64_str is None:
            return None

        # Get user credentials
        user_email, user_pwd = self.extract_user_credentials(base64_str)
        if user_email is None or user_pwd is None:
            return None

        # Get user objec from credentials
        user = self.user_object_from_credentials(user_email, user_pwd)

        return user
