import os

from jinja2 import Environment, FileSystemLoader, select_autoescape

jinja_env = Environment(
    loader=FileSystemLoader("/usr/src/app/hancock/templates/comms"),
    autoescape=select_autoescape(),
)


def render(template, context):
    t = jinja_env.get_template(template)
    return t.render(**context)


def send_email(template, *recipient, **context):
    plain = render(f"email/{template}.txt", context)
    html = render(f"email/{template}.html", context)

    if os.environ.get("SMTP_HOST"):
        # TODO: Add SMTP integration
        pass
    else:
        print(plain)
