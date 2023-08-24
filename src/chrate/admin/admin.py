from functools import wraps
from flask import request
from flask_login.config import EXEMPT_METHODS

def role_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method in EXEMPT_METHODS:
            pass

        # TODO: check for admin
        # TODO: ask mom for one-colum tables

        return func(*args, **kwargs)

    return wrapper
