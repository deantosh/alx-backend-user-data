#!/usr/bin/env python3
"""
Create one function for each of the following tasks. Use the requests
module to query your web server for the corresponding end-point.
"""
import requests


BASE_URL = "http://127.0.0.1:5000"  # Replace with your server's addr


def register_user(email: str, password: str) -> None:
    """Registers a new user with the provided email and password."""
    response = requests.post(
        f"{BASE_URL}/users", json={"email": email,
                                   "password": password})
    assert response.status_code == 201,
    f"Expected 201, got {response.status_code}"
    payload = response.json()
    assert payload == {"email": email, "message": "user created"},
    f"Unexpected payload: {payload}"


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempts to log in with the wrong password."""
    response = requests.post(f"{BASE_URL}/sessions", json={
        "email": email, "password": password})
    assert response.status_code == 401,
    f"Expected 401, got {response.status_code}"


def log_in(email: str, password: str) -> str:
    """Logs in with the correct credentials and returns the session ID."""
    response = requests.post(f"{BASE_URL}/sessions",
                             json={"email": email,
                                   "password": password})
    assert response.status_code == 200,
    f"Expected 200, got {response.status_code}"
    payload = response.json()
    assert "session_id" in payload,
    f"Expected session_id in response, got {payload}"
    return payload["session_id"]


def profile_unlogged() -> None:
    """Attempts to access the profile endpoint without being
       logged in.
    """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403,
    f"Expected 403, got {response.status_code}"


def profile_logged(session_id: str) -> None:
    """Accesses the profile endpoint with a valid session ID."""
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200,
    f"Expected 200, got {response.status_code}"
    payload = response.json()
    assert "email" in payload,
    f"Expected email in response, got {payload}"


def log_out(session_id: str) -> None:
    """Logs out the user by invalidating the session ID."""
    cookies = {"session_id": session_id}
    response = requests.delete(
        f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200,
    f"Expected 200, got {response.status_code}"
    payload = response.json()
    assert payload == {"message": "session deleted"},
    f"Unexpected payload: {payload}"


def reset_password_token(email: str) -> str:
    """Requests a password reset token for the user."""
    response = requests.post(f"{BASE_URL}/reset_password",
                             json={"email": email})
    assert response.status_code == 200,
    f"Expected 200, got {response.status_code}"
    payload = response.json()
    assert "reset_token" in payload,
    f"Expected reset_token in response, got {payload}"
    return payload["reset_token"]


def update_password(
        email: str, reset_token: str, new_password: str) -> None:
    """Updates the user's password using the reset token."""
    response = requests.put(
        f"{BASE_URL}/reset_password",
        json={"email": email, "reset_token": reset_token,
              "new_password": new_password}
    )
    assert response.status_code == 200,
    f"Expected 200, got {response.status_code}"
    payload = response.json()
    assert payload == {"email": email,
                       "message": "password updated"},
    f"Unexpected payload: {payload}"


# Configuration for the test
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
