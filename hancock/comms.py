import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from flask_mail import Mail as FlaskMail, Message

mail = FlaskMail()


def init_app(app):
    mail.init_app(app)


jinja_env = Environment(
    loader=FileSystemLoader("/usr/src/app/hancock/templates/comms"),
    autoescape=select_autoescape(),
)


def render(template, context):
    t = jinja_env.get_template(template)
    return t.render(**context)


def send_email(template, subject, *recipient, **context):
    plain = render(f"email/{template}.txt", context)
    html = render(f"email/{template}.html", context)

    if os.environ.get("MAIL_PASSWORD"):
        message = Message(
            recipients=list(recipient),
            subject=f"[AXS-Signature] {subject}",
            body=plain,
            html=html,
        )
        mail.send(message)
    else:
        print(plain)
