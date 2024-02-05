# apps/settings.py

import logging
import os
from datetime import datetime

try:
    from .settings_local import *
except ImportError:
    pass

DEBUG = True
ALLOWED_HOSTS = ["*"]
SECRET_KEY = "utx_secret_key"
TIME_ZONE = os.environ["UTX_TIME_ZONE"]


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
        "utx_logs_fils": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(
                log_dir, "{:%Y%m%d}_utx.log".format(datetime.now())
            ),
            "when": "midnight",
            "backupCount": 7,  # Keep up to 7 days of logs
            "formatter": "verbose",
        },
        "utx_db_logs_fils": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": os.path.join(
                log_dir, "{:%Y%m%d}_utx_db.log".format(datetime.now())
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
            "handlers": ["utx_logs_fils", "console"],
            # "handlers": ["utx_logs_fils", "utx_db_logs_fils"],
            "level": "INFO",  # Adjust the log level as needed
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["utx_db_logs_fils", "console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
    "formatters": {
        "verbose": {
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": "{levelname:<5} {asctime:<5} {class_name}.{method_name}: {message}",
        },
    },
}


INSTALLED_APPS = [
    "apps.brokers",
    "apps.data",
    "apps.strategies",
    "apps.utils",
    "apps.tests",
]


class ClassNameFilter(logging.Filter):
    def filter(self, record):
        if not hasattr(record, "class_name"):
            record.class_name = record.name
            record.method_name = record.funcName
        return True


LOGGING["filters"] = {
    "class_name_filter": {
        "()": ClassNameFilter,
    },
}

LOGGING["handlers"]["utx_logs_fils"]["filters"] = ["class_name_filter"]
LOGGING["handlers"]["utx_db_logs_fils"]["filters"] = ["class_name_filter"]
LOGGING["handlers"]["console"]["filters"] = ["class_name_filter"]
