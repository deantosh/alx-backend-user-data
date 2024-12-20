#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})


auth = os.getenv('AUTH_TYPE', None)
if auth == 'basic_auth':
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
else:
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.before_request
def filter_each_request():
    """Filters each request in application"""
    excluded_paths = [
        '/api/v1/status/', '/api/v1/unauthorized/', '/api/v1/forbidden/']

    if auth is None:
        return

    # If in excluded paths - no authentication needed
    if not auth.require_auth(request.path, excluded_paths):
        return

    # If authorization header not provided
    if auth.authorization_header(request) is None:
        abort(401)

    # Check if user is valid
    if auth.current_user(request) is None:
        abort(403)


@app.errorhandler(401)
def not_authorized(error) -> str:
    """ Unauthorized access
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(403)
def access_forbidden(error) -> str:
    """ User access forbidden
    """
    return jsonify({'error': 'Forbidden'}), 403


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
