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
        return jsonify({
            "email": user.email, "message": "user created"})
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
        response.set_cookie('session_id', ssession_id)

        return response

    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout_user():
    """Logout user"""
    # Get session id from cookie
    session_id = request.cokkies.get('session_id')

    # Get user from session id
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)

    # Destroy session
    AUTH.destroy_session(user.id)

    return redirect(url_for('index_page'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
