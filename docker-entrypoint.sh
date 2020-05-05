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

if [ "$1" == "runserver" ]; then
    echo "Running migrations"
    python manage.py migrate

    echo "Running collectstatic"
    python manage.py collectstatic --noinput

    create_superuser

    exec python manage.py "$@"
fi
