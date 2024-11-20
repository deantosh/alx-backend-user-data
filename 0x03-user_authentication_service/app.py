#!/usr/bin/env python3
"""
Simple basic application
"""
from flask import Flask, jsonify


app = Flask()


@app.route("/", methods=["GE"], strict_slashes=False)
def index_page():
    """Default route"""
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
