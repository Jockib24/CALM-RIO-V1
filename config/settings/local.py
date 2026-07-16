from .base import *  # noqa

# Local development settings
DEBUG = True

# INSTALLED_APPS += ["django_extensions"]  # noqa (temp disabled — no network)

# SQLite for local dev (in base.py already)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # noqa
    }
}
