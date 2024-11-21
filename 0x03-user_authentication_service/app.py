#!/usr/bin/env python3
"""
Simple basic application
"""
from auth import Auth
from flask import Flask, request, jsonify


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
