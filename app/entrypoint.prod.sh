#!/bin/sh

if [[ -n "${POSTGRES_HOST}" ]]; then
    echo "Waiting for postgres..."

    while ! nc -z $POSTGRES_HOST 5432; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"
