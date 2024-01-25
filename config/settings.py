# config/settings.py

import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

try:
    from .settings_local import *
except ImportError:
    pass

SECRET_KEY = "utx_secret_key"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Set the log directory path
log_dir = os.path.join("data", "logs")

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
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "INFO",  # Adjust the log level as needed
            "propagate": True,
        },
        "django.db.backends": {
            "handlers": ["debug_file"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
}
