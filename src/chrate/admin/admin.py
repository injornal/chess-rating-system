from functools import wraps
from flask import request, flash, redirect, url_for
from flask_login.config import EXEMPT_METHODS
from flask_login import current_user
from sqlalchemy.orm import Session
from sqlalchemy import select
from chrate.model.rating import engine, Roles


def role_required(role="ADMIN"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if request.method in EXEMPT_METHODS:
                pass
            with Session(engine) as session:
                query = select(Roles).where(Roles.name == role)
                role_instance = session.execute(query).first()[0]
            if current_user.role_id == role_instance.id:
                return func(*args, **kwargs)
            else:
                return "Access denied", 403
        return wrapper
    return decorator
