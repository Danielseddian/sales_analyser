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

celery -A settings purge -f # Очистка задач, если не были выполнены вовремя.

celery -A settings worker --beat -l INFO --concurrency 1 -E
