#!/bin/bash

create_superuser="
import django
django.setup()
from django.contrib.auth.models import User
try:
    User.objects.create_superuser('$DJANGO_SUPERUSER_NAME', '$DJANGO_SUPERUSER_MAIL', '$DJANGO_SUPERUSER_PASS')
except Exception:
    pass
"

create_superuser() {
    if [ -z "$DJANGO_SUPERUSER_NAME" ] || [ -z "$DJANGO_SUPERUSER_MAIL" ] || [ -z "$DJANGO_SUPERUSER_PASS" ]; then
        echo "Environment variables for database not set, not creating superuser."
    else
        echo "Creating superuser"
        python -c "$create_superuser"
    fi
}

wait_for_db() {
    if [ -z "$DJANGO_DB_HOST" ] || [ -z "$DJANGO_DB_PORT" ]; then
        echo "No django database host or port, not waiting for db."
    else
        echo "Waiting for database"
        dockerize -wait tcp://"$DJANGO_DB_HOST":"$DJANGO_DB_PORT" -timeout 30s
    fi
}

if [ "$1" == "runserver" ]; then
    wait_for_db

    echo "Running migrations"
    python manage.py migrate

    echo "Running collectstatic"
    python manage.py collectstatic --noinput

    create_superuser

    exec python manage.py "$@"
fi
