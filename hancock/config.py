import os

FLASK_ENV = os.environ.get("FLASK_ENV", "development")

MAIL_DEBUG = FLASK_ENV == "development"
MAIL_DEFAULT_SENDER = os.environ.get(
    "MAIL_DEFAULT_SENDER",
    "AXS Signature <mail@axs-signature.co>",
)
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", None)
MAIL_PORT = os.environ.get("MAIL_PORT", 587)
MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.sendgrid.net")
MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "apikey")
MAIL_USE_SSL = bool(os.environ.get("MAIL_USE_SSL", False))
MAIL_USE_TLS = bool(os.environ.get("MAIL_USE_TLS", True))
