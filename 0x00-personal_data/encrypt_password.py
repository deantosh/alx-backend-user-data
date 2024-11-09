#!/usr/bin/env python3
"""
Task 5:;
Implement a hash_password function that expects one string argument name
password and returns a salted, hashed password, which is a byte string.

Use the bcrypt package to perform the hashing (with hashpw).

Task 6:
Implement an is_valid function that expects 2 arguments and returns a boolean.

Arguments:
 - hashed_password: bytes type
 - password: string type

Use bcrypt to validate that the provided password matches the hashed password.
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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if passweord and hashed_password match

    Args:
        hashed_password - encrypted password
        password - Plain password (string)

    Returns:
        True: Match
        False: Not a  match
    """
    return bcrypt.checkpw(password.encode('UTF-8'), hashed_password)
