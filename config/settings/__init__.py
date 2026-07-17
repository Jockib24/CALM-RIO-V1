"""
Settings loader.

By default, loads local development settings.
In production, set DJANGO_SETTINGS_MODULE=config.settings.production
"""
import os
import sys

if os.environ.get("DJANGO_SETTINGS_MODULE") == "config.settings.production":
    from .production import *  # noqa
elif os.environ.get("DJANGO_ENV") == "production":
    from .production import *  # noqa
else:
    from .local import *  # noqa
