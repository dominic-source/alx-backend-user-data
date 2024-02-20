#!/usr/bin/env python3
"""
Main file
"""
import requests


def register_user(email: str, password: str) -> None:
    """register user using the request module"""
    url = "http://localhost:5000/users"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    ds = response.json()
    assert 200 == int(response.status_code)
    assert ds == {'email': email, 'message': 'user created'}


def log_in_wrong_password(email: str, password: str) -> None:
    """Login wrong password"""
    url = "http://localhost:5000/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert 401 == int(response.status_code)


def log_in(email: str, password: str) -> str:
    """Login a user"""
    url = "http://localhost:5000/sessions"
    data = {"email": email, "password": password}
    response = requests.post(url, data=data)
    assert 200 == int(response.status_code)
    assert response.json() == {"email": email, "message": "logged in"}
    return response.cookies["session_id"]


def profile_unlogged() -> None:
    """unlogged profile"""
    url = "http://localhost:5000/profile"
    response = requests.get(url)
    assert 403 == int(response.status_code)


def profile_logged(session_id: str) -> None:
    """Logged profile testing"""
    url = "http://localhost:5000/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert 200 == int(response.status_code)
    assert "email" in response.json()


def log_out(session_id: str) -> None:
    """log out users"""
    url = "http://localhost:5000/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """reset password"""
    url = "http://localhost:5000/reset_password"
    data = {"email": email}
    response = requests.post(url, data=data)
    dt = response.json()
    assert 200 == response.status_code
    return dt.get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update password"""
    url = "http://localhost:5000/reset_password"
    data = {"email": email, "reset_token": reset_token,
            "new_password": new_password}
    response = requests.put(url, data=data)
    dt = response.json()
    assert 200 == response.status_code
    assert dt == {"email": email, "message": "Password updated"}


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
