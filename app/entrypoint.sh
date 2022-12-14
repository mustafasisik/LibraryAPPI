#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#python manage.py flush --no-input
python manage.py migrate --noinput # migrate at first
python manage.py makemmigrations
python manage.py migrate --noinput # migrate at first
python manage.py collectstatic --noinput # collect static data for nginx
python manage.py create_admin # create a super user
python manage.py create_library_user # create a default user


exec "$@"