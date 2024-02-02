# config/settings.py

import logging
import os
from datetime import datetime

try:
    from .settings_local import *
except ImportError:
    pass

SECRET_KEY = "utx_secret_key"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DJANGO_DB_NAME", "default_database"),
        "USER": os.getenv("DJANGO_DB_USER", "default_user"),
        "PASSWORD": os.getenv("DJANGO_DB_PASSWORD", "default_password"),
        "HOST": os.getenv("DJANGO_DB_HOST", "localhost"),
        "PORT": os.getenv("DJANGO_DB_PORT", "5432"),
    }
}

# Set the log directory path
log_dir = os.path.join("", "logs")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(
                log_dir, "{:%Y%m%d}_utx.log".format(datetime.now())
            ),
            "when": "midnight",
            "backupCount": 7,  # Keep up to 7 days of logs
            "formatter": "verbose",
        },
        "debug_file": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(
                log_dir, "{:%Y%m%d}_dbg_utx.log".format(datetime.now())
            ),
            "when": "midnight",
            "backupCount": 7,  # Keep up to 7 days of logs
            "formatter": "verbose",
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["debug_file", "console"],
            # "handlers": ["file", "debug_file"],
            "level": "INFO",  # Adjust the log level as needed
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
    "formatters": {
        "verbose": {
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": "{levelname} {asctime}  {class_name}.{method_name}: {message}",
        },
    },
}

INSTALLED_APPS = [
    "apps.brokers",
    "apps.config",
    "apps.data",  # Include the app name, not the model path
    "apps.strategies",
    "apps.utils",
]


class ClassNameFilter(logging.Filter):
    def filter(self, record):
        record.class_name = record.name
        record.method_name = record.funcName
        return True


LOGGING["filters"] = {
    "class_name_filter": {
        "()": ClassNameFilter,
    },
}

LOGGING["handlers"]["file"]["filters"] = ["class_name_filter"]
LOGGING["handlers"]["debug_file"]["filters"] = ["class_name_filter"]
LOGGING["handlers"]["console"]["filters"] = ["class_name_filter"]
