#!/usr/bin/env python3

"""Module to manage session"""
import os
from api.v1.views import app_views
from flask import request, make_response, jsonify
from models.user import User


@app_views.route('/auth_session/login', methods=["POST"], strict_slashes=False)
def session_post() -> str:
    """listen for post request"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400
    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user[0].id)
    response = make_response(jsonify(user[0].to_json()))
    response.set_cookie(os.environ.get("SESSION_NAME"), session_id)
    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def del_session() -> str:
    """Delete a user session"""
    from api.v1.app import auth
    destroy = auth.destroy_session(request)
    if not destroy:
        abort(404)
    return jsonify({}), 200
