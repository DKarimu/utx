import logging
import os
from datetime import datetime

DEBUG = True
ALLOWED_HOSTS = ["*"]
SECRET_KEY = "utx_secret_key"
TIME_ZONE = os.getenv("UTX_TIME_ZONE", "UTC")

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

LOG_DIR = os.path.join(os.path.dirname("app"), "logs")
LOG_FILE_FORMAT = "{:%Y%m%d}_utx.log".format(datetime.now())
LOG_DB_FILE_FORMAT = "{:%Y%m%d}_utx_db.log".format(datetime.now())

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)


def get_timed_rotating_file_handler(filename, level="DEBUG"):
    return {
        "level": level,
        "class": "logging.handlers.TimedRotatingFileHandler",
        "filename": os.path.join(LOG_DIR, filename),
        "when": "midnight",
        "backupCount": 7,
        "formatter": "verbose",
        "filters": ["class_name_filter"],
    }


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "class_name_filter": {
            "()": "apps.settings.ClassNameFilter",
        },
    },
    "handlers": {
        "utx_logs_file": get_timed_rotating_file_handler(LOG_FILE_FORMAT),
        "utx_db_logs_file": get_timed_rotating_file_handler(LOG_DB_FILE_FORMAT),
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
            "filters": ["class_name_filter"],
        },
    },
    "loggers": {
        "django": {
            "handlers": ["utx_logs_file", "console"],
            "level": "INFO",
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["utx_db_logs_file", "console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "formatters": {
        "verbose": {
            "style": "{",
            "datefmt": "%Y.%m.%d %H:%M:%S",
            "format": "{levelname:<5} {asctime} {class_name}.{method_name}: {message}",
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
        record.class_name = getattr(record, "class_name", record.name)
        record.method_name = getattr(record, "method_name", record.funcName)
        return True
