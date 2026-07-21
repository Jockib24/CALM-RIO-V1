import os

from .base import *  # noqa

# ---------------------------------------------------------------
# PRODUCTION SETTINGS — o2switch shared hosting
# ---------------------------------------------------------------
DEBUG = False

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", ".calm-rio.com"
).split(",")

# ---------- Security ----------
SECURE_SSL_REDIRECT = (
    os.environ.get("DJANGO_SECURE_SSL_REDIRECT", "True").lower() == "true"
)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = os.environ.get(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "https://*.calm-rio.com",
).split(",")
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# ---------- Database ----------
# Supports: postgresql://, mysql://, sqlite:// via DATABASE_URL
import dj_database_url  # noqa

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ["DATABASE_URL"],
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ---------- Static & Media ----------
# BASE_DIR-relative paths (no hardcoded /vol/ paths)
STATIC_ROOT = os.environ.get(
    "STATIC_ROOT",
    str(BASE_DIR / "staticfiles"),  # noqa
)
MEDIA_ROOT = os.environ.get(
    "MEDIA_ROOT",
    str(BASE_DIR / "media"),  # noqa
)

# Whitenoise: compressed + cache-busted static files
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ---------- Email ----------
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True").lower() == "true"

# ---------- Logging ----------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": os.environ.get("DJANGO_LOG_LEVEL", "WARNING"),
    },
}
