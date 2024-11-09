#!/usr/bin/env python3
"""
Implement a hash_password function that expects one string argument name
password and returns a salted, hashed password, which is a byte string.

Use the bcrypt package to perform the hashing (with hashpw).
"""
import bcrypt


def hash_password(name: str) -> bytes:
    """Encrypts the password using bcrypt algorithm

    Args:
        name (str): The plaintext password to hash.

    Returns:
        bytes: The bcrypt hashed password.
    """
    # convert string to binary
    password = name.encode('UTF-8')

    # Generate salt and hash the password
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password, salt)

    return hash_password
