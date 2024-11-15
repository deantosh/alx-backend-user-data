#!/usr/bin/env python3
"""Module for Session views
"""
from api.v1.views import app_views
from flask import request, jsonify, make_response
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def user_login():
    """Login authenticated user to application"""
    # Retrieve user credentials
    email = request.form.get('email')
    if email is None:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if password is None:
        return jsonify({"error": "password missing"}), 400

    # Search user instance based on email
    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    # Get user
    user = users[0]

    # Check password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create SessionID for the user
    from api.v1.app import auth  # avoid circular imports

    session_id = auth.create_session(user.id)
    if session_id is None:
        return jsonify({"error": "unable to create session"}), 500

    # Create the response and set the session cookie
    session_name = os.getenv('SESSION_NAME')
    response = make_response(jsonify(user.to_json()))
    response.set_cookie(session_name, session_id)

    return response
