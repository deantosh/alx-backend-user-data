#!/usr/bin/env python3
"""
Simple basic application
"""
from auth import Auth
from flask import Flask, request, jsonify, make_response, abort


AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index_page():
    """Default route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def register_user():
    """Creates a new user"""

    # Get email and password
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # Attempt to register a user
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        # If user is already registered
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """User login"""

    # Get user credentials
    email = request.form.get('email')
    password = request.form.get('password')

    # Verify the user logging in
    result = AUTH.valid_login(email, password)
    if result:
        # Create a session and store in both and cookie
        session_id = AUTH.create_session(email)

        response = make_response(
            jsonify({"email": email, "message": "logged in"}))
        response.set_cookie('session_id', session_id)

        return response

    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Logout user"""
    # Get session id from cookie
    session_id = request.cookies.get('session_id')

    # Get user from session id
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    # Destroy session
    AUTH.destroy_session(user.id)

    return redirect(url_for('index_page'))


@app.route('/profile', methods=["GET"], strict_slashes=False)
def user_profile():
    """Display user profile"""
    session_id = request.cookies.get("session_id")

    # Retrieve user
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Reset user password token"""

    # Get form data
    email = request.form.get('email')

    try:
        # Find user using email
        reset_token = AUTH.get_reset_password_token(email)

        return jsonify(
            {"email": email, "reset_token": reset_token}), 200
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=['PUT'], strict_slashes=False)
def update_password():
    """Update user password"""

    # Retrieve form data
    email = request.form.get('email')
    reset_token = request.form.get('reset_token')
    new_password = request.form.get('new_password')

    try:
        # Update user password
        AUTH.update_password(reset_token, new_password)

        return jsonify(
            {"email": email, "message": "Password updated"}), 200
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
