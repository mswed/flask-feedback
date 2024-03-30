from flask import session


def authorize(username):
    if 'username' in session:
        return session['username'] == username

    return False
