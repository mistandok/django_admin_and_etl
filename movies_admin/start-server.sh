#!/bin/sh

if [ ${DB_TYPE} = "postgres" ]
then
  echo "Waiting for PostgreSQL..."

  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

python ./manage.py migrate
python ./manage.py createsuperuser_if_none_exists --user=admin --password=admin
exec gunicorn config.wsgi:application --bind $GUNICORN_HOST:$GUNICORN_PORT

exec "$@"