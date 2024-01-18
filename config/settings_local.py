# config/settings_local.py

import os

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DJANGO_DB_NAME', 'default_database'),
        'USER': os.getenv('DJANGO_DB_USER', 'default_user'),
        'PASSWORD': os.getenv('DJANGO_DB_PASSWORD', 'default_password'),
        'HOST': os.getenv('DJANGO_DB_HOST', 'localhost'),
        'PORT': os.getenv('DJANGO_DB_PORT', '5432'),
    }
}

# You can add more settings or overrides specific to your local environment if needed
