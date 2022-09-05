import json
import time
from uuid import uuid4

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
    send_from_directory,
)
from hancock.schema import CreateSessionSchema

# TODO: Error pages like 404 if the sid is wrong
# TODO: Error handling, if the form submission is wrong
# TODO: Turn off CORS for the create session route
# TODO: Show session ID to user on sign page and on creator's page alongside loading indicator
# TODO: Redirect URI should always be accessible to user, and can be used to verify the signature request (rel=nooperner)


bp = Blueprint("hancock", __name__)


@bp.route("/", methods=["GET"])
def home():
    """A really simple introduction page, with a form that you can use to
    create a signature session to test things out."""
    return render_template("home.html")


def make_sid(data):
    # TODO: Hash the declaration and signee_email and make it the ID, then you can compare the signature file with the hash of what was signed for
    return uuid4()


@bp.route("/session/", methods=["POST"])
def create_session():
    input = request.get_json(silent=True)
    if not input and request.form:
        input = CreateSessionSchema.from_form(request.form)
    input = CreateSessionSchema(**input).dict(exclude={"api_key"})
    input["created_on"] = time.time()
    # TODO: Get org name from API key
    input["created_by"] = "Demo Organisation"
    input["signed_on"] = None
    sid = make_sid(input)
    with open(f"/data/signatures/{sid}.json", "w") as fp:
        json.dump(input, fp)
    return redirect(url_for("hancock.sign", sid=sid))


@bp.route("/session/<sid>/", methods=["GET", "POST"])
def sign(sid):
    with open(f"/data/signatures/{sid}.json", "r") as fp:
        details = json.load(fp)
    if details["signed_on"]:
        return redirect(url_for("hancock.get_signature", sid=sid))
    if request.method == "POST":
        # TODO: Check CSRF token
        with open(f"/data/signatures/{sid}.svg", "wb") as fp:
            request.files["signature"].save(fp)
        with open(f"/data/signatures/{sid}.json", "w") as fp:
            details["signed_on"] = time.time()
            json.dump(details, fp)
        return redirect(url_for("hancock.session_close", sid=sid))
    return render_template("sign.html", sid=sid, details=details)


@bp.route("/session/<uuid:sid>/close/", methods=["GET"])
def session_close(sid):
    # TODO: Can we force the browser to open the opener tab when we close the child?
    with open(f"/data/signatures/{sid}.json", "r") as fp:
        details = json.load(fp)
    return render_template("close.html", redirect_uri=details["redirect_uri"])


@bp.route("/signature/<uuid:sid>/", methods=["GET"])
def get_signature(sid):
    # TODO: verify hash in query string
    # TODO: Also show the declaration and things like that?
    # colour signature according to query string params?
    return send_from_directory(
        "/data/signatures/",
        f"{sid}.svg",
        as_attachment=False,
    )
