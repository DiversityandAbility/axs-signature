import base64
import hashlib
import json
import os
import tempfile
import time

from flask import (
    abort,
    make_response,
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
    send_from_directory,
    jsonify,
)
from fontTools.subset import main as ft_subset
from flask_cors import cross_origin
from hancock import comms, security
from werkzeug.utils import secure_filename
from hancock.schema import CreateSessionSchema

# TODO: Error pages like 404 if the sid is wrong
# TODO: Error handling, if the form submission is wrong


bp = Blueprint("hancock", __name__)


@bp.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@bp.route("/demo/", methods=["GET"])
def demo():
    return render_template(
        "demo.html",
        name=request.args.get("name", ""),
        email=request.args.get("email", ""),
        sessionId=request.args.get("sid", ""),
    )


@bp.route("/terms/", methods=["GET"])
def terms():
    return redirect(
        "https://docs.google.com/document/d/1GR0nUVOlmumWpyXklfGeTs3DM4P9E4g4ekdDYvuQf88/edit?usp=sharing"
    )


@bp.route("/privacy/", methods=["GET"])
def privacy():
    return redirect("https://diversityandability.com/privacy-notice/")


@bp.route("/emails/<name_text>.txt")
@bp.route("/emails/<name_html>/")
def email_preview(name_html=None, name_text=None):
    if name_html:
        return render_template(f"comms/email/{name_html}.html", **request.args)
    content = render_template(f"comms/email/{name_text}.txt", **request.args)
    resp = make_response(content, 200)
    resp.content_type = "text/plain"
    return resp


def make_sid(details):
    h = hashlib.blake2b(digest_size=16)
    h.update(details["title"].encode("utf8"))
    h.update(details["declaration"].encode("utf8"))
    h.update(details["signee_email"].encode("utf8"))
    h.update(str(details["created_on"]).encode("utf8"))
    return h.hexdigest()


def check_key(key):
    # TODO: Have an actual DB of API keys
    # TODO: Time limited API keys, connected to the signee_email, use once?
    if key != "rah8aeph5xate2reeNgohpeigoonot3ieteefiekequae2oozieghieThooghub4":
        abort(401)
    return {"name": "Demo Organisation"}


def check_hash(sid, hash):
    h_cmp = hashlib.blake2b(digest_size=16)
    h_cmp.update(sid.encode("utf8"))
    h_cmp.update(os.environ["SECRET_KEY"].encode("utf8"))
    h_cmp = h_cmp.hexdigest()
    return hash == h_cmp


@bp.route("/session/", methods=["POST"])
@cross_origin()
def create_session():
    key = request.headers.get("X-Api-Key")
    org = check_key(key)
    details = request.get_json()
    details = CreateSessionSchema(**details).dict()
    details["created_on"] = time.time()
    details["created_by"] = org["name"]
    details["signed_on"] = None
    sid = make_sid(details)
    with open(f"/data/signatures/{sid}.json", "w") as fp:
        json.dump(details, fp)
    h = hashlib.blake2b(digest_size=16)
    h.update(sid.encode("utf8"))
    h.update(os.environ["SECRET_KEY"].encode("utf8"))
    h = h.hexdigest()
    comms.send_email(
        "signature_requested",
        f"Your signature is needed on '{details['title']}'",
        details["signee_email"],
        url=url_for(
            "hancock.sign",
            sid=sid,
            h=h,
            _external=True,
            _scheme="https",
        ),
        org=details["created_by"],
        doc=details["title"],
    )
    return jsonify({"status": 201, "data": {"sid": sid}}), 201


@bp.route("/session/<sid>/", methods=["GET", "POST"])
@security.requires_csrf
def sign(sid):
    if not check_hash(sid, request.args.get("h", "")):
        return redirect(url_for("hancock.error"))

    with open(f"/data/signatures/{sid}.json", "r") as fp:
        details = json.load(fp)
    if details["signed_on"]:
        # TODO: This needs to redirect to an HTML page that shows the signature.
        return redirect(url_for("hancock.get_signature", sid=sid))
    if request.method == "POST":
        with open(f"/data/signatures/{sid}.svg", "w") as fp:
            fp.write(request.form["signature"])
        with open(f"/data/signatures/{sid}.json", "w") as fp:
            details["signed_on"] = time.time()
            json.dump(details, fp)
        return redirect(url_for("hancock.get_signature", sid=sid))
    return render_template(
        "sign.html",
        sid=sid,
        details=details,
        cursivefont=get_font("cursive"),
        monofont=get_font("monospace", chars="1234567890:/,qwertyuiopasdfghjklzxcvbnm"),
    )


def get_safe_details(sid):
    with open(f"/data/signatures/{sid}.json", "r") as fp:
        details = json.load(fp)
    safe_details = {
        "status": "PENDING",
        "title": details["title"],
        "declaration": details["declaration"],
        "created_on": details["created_on"],
        "created_by": details["created_by"],
        "signed_on": details["signed_on"],
    }
    if details["signed_on"]:
        safe_details["status"] = "SIGNED"
    return safe_details


@bp.route("/signature/<sid>/", methods=["GET"])
def get_signature(sid):
    details = get_safe_details(sid)
    return render_template("signature.html", sid=sid, details=details)


@bp.route("/signature/<sid>.svg", methods=["GET"])
def get_signature_svg(sid):
    # TODO: colour signature according to query string params?
    return send_from_directory(
        "/data/signatures/",
        f"{sid}.svg",
        as_attachment=False,
    )


@bp.route("/signature/<sid>.json", methods=["GET"])
def get_signature_details(sid):
    return jsonify({"data": get_safe_details(sid)})


@bp.route("/error/", methods=["GET"])
def error():
    return render_template("error.html")


def get_font(name, chars=None):
    path = f"/data/fonts/{name}.woff2"

    bytes_ = None
    if chars:
        with tempfile.NamedTemporaryFile() as fp:
            chars = "".join(sorted(set(chars)))
            ft_subset(
                [
                    path,
                    f"--text={chars}",
                    f"--output-file={fp.name}",
                    "--flavor=woff2",
                ]
            )
            fp.seek(0)
            bytes_ = fp.read()
    else:
        with open(path, "rb") as fp:
            bytes_ = fp.read()

    as_b64 = base64.b64encode(bytes_)
    return {
        "font": name,
        "chars": chars,
        "base64": as_b64.decode("utf8").replace("\n", ""),
    }


@bp.route("/subset/", methods=["GET"])
def subset_font():
    # TODO: Auth this route somehow, so people can't just use it as a subsetting tool?
    font_name = request.args.get("font", "cursive")
    font_name = secure_filename(font_name)
    chars = request.args.get("chars", None)
    return jsonify({"status": 200, "data": get_font(font_name, chars)})
