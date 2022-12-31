#!/bin/sh

if [ ${DB_TYPE} = "postgres" ]
then
  echo "Waiting for PostgreSQL..."

  while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
  done

  echo "PostgreSQL started"
fi

if [ ${TARGET_DB_TYPE} = "elasticsearch" ]
then
  echo "Waiting for Elasticsearch..."

  while ! nc -z $ES_HOST $ES_PORT; do
    sleep 0.1
  done

  echo "Elasticsearch started"
fi

python ./start.py

exec "$@"