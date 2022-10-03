from functools import wraps
import secrets
from flask import request, session, abort


def requires_csrf(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.method == "POST":
            incoming = request.form.get("csrf_token", "")
            required = session.get("csrf_token", secrets.token_hex(32))
            if incoming != required:
                abort(403)
        session["csrf_token"] = secrets.token_hex(32)
        return func(*args, **kwargs)

    return wrapper
