#!/bin/bash

# Verify database connection
check_db_connection() {
  psql -h "$DJANGO_DB_HOST" -p "$DJANGO_DB_PORT" -U "$DJANGO_DB_USER" -d "$DJANGO_DB_NAME" -c "SELECT 1;" >/dev/null 2>&1
  if [ $? -eq 0 ]; then
    echo "Database connection successful!"
  else
    echo "Error: Unable to connect to the database."
    exit 1
  fi
}

# Check database connection
check_db_connection

# Migrate the database
python manage.py migrate

# Run the Django development server
python manage.py runserver 0.0.0.0:8080
