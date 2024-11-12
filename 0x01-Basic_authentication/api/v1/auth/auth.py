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
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # format path and add ending / if no found
        if not path.endswith('/'):
            path = path + '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """Not implemented"""
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Not implemented"""
        return None
