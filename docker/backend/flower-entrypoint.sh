#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
    sleep 2
done


until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

python manage.py create_cache_table

celery -A settings flower --loglevel=DEBUG --port=5555 --basic_auth=${FLOWER_USER}:${FLOWER_PASSWORD}
