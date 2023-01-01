#!/bin/sh

wait_database()
{
  HOST=$1
  PORT=$2
  TYPE=$3

  echo "Waiting for $TYPE..."

  while ! nc -z $HOST $PORT; do
    sleep 0.1
  done

  echo "$TYPE started"
}

if [ ${DB_TYPE} = "postgres" ]
  then
    wait_database $DB_HOST $DB_PORT $DB_TYPE
fi

if [ ${TARGET_DB_TYPE} = "elasticsearch" ]
  then
    wait_database $ES_HOST $ES_PORT $TARGET_DB_TYPE
fi

if [ ${STATE_STORAGE_TYPE} = "redis" ]
  then
    wait_database $REDIS_HOST $REDIS_PORT $STATE_STORAGE_TYPE
fi

python ./start.py

exec "$@"