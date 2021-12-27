#!/bin/bash

echo 'Collect static files...'
python manage.py collectstatic --no-input --clear

# Check if database is ready
while ! python manage.py migrate --no-input; do
    echo 'Waiting for database....'
    sleep 3s
done

# Create a default superuser account
echo 'Create a default superuser account...'
python manage.py defaultsuperuser

# Run gunicorn server
echo 'Start Gunicorn server...'
gunicorn --bind 0.0.0.0:8000 --workers 3 config.wsgi
