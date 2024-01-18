# config/settings.py

import os

SECRET_KEY = 'your_secret_key'
DEBUG = False
ALLOWED_HOSTS = ['*'] 

try:
    from .settings_local import *
except ImportError:
    pass
