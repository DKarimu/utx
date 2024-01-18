#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
  export $(cat .env | grep -v '#' | awk '/=/ {print $1}')
fi

# Migrate the database
python manage.py migrate

# Run the Django development server
python manage.py runserver 0.0.0.0:8080
