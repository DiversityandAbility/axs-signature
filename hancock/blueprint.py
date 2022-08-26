import functools
from uuid import uuid4

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)


bp = Blueprint("hancock", __name__)


@bp.route("/", methods=["GET"])
def welcome():
    # Show a welcome/landing page
    # For now, redirect to fake signature
    uuid = uuid4()
    return redirect(url_for("hancock.sign", sid=uuid))


@bp.route("/session/", methods=["POST"])
def create_session():
    # Auth the entity creating the session
    # Take in details about the session signature
    # Create a placeholder signature file. Only the provided details, no signature yet
    uuid = uuid4()
    return redirect(url_for("hancock.sign", sid=uuid))


@bp.route("/session/<uuid:sid>/", methods=["GET", "POST"])
def sign(sid):
    # Load details from placeholder file
    # If placeholder filled in with signature, redirect to that signature
    # If POST, verify then save siganture, redirect to provided redirect_uri
    # If GET, grab details from placeholder, show template
    return render_template("sign.html", sid=sid)


@bp.route("/signature/<uuid:sid>/", methods=["GET"])
def get_signature(sid):
    # verify hash in query string
    # colour signature according to query string params?
    return "SIGNATURE"
