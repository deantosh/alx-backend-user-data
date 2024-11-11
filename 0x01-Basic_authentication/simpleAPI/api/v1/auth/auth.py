#!/usr/bin/env python3
"""
Implement a class to manage the API authentication.
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """Defines a Base class Auth
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Not implemented"""
        return False

    def authorization_header(self, request=None) -> str:
        """Not implemented"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Not implemented"""
        return None