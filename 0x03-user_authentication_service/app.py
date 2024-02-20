#!/usr/bin/env python3

"""Basic flask application"""

import flask
from flask import Flask, jsonify, request, make_response
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def first_req() -> str:
    """return json str"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """register user"""
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """Login users"""
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        if not session_id:
            flask.abort(401)
        response = make_response(jsonify({"email": email,
                                          "message": "logged in"}))
        response.set_cookie("session_id", session_id)
        return response
    flask.abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
