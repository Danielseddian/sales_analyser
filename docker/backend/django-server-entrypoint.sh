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

mode=$(echo "${DEBUG_MODE}" | tr '[:upper:]' '[:lower:]')
case "${mode}" in
    "true" | "yes" | "y" | "1")
        echo "Running server in debug mode"
        ;;
    *)
        python manage.py collectstatic --noinput
        ;;
esac

uvicorn settings.asgi:application --host 0.0.0.0 --port 8000
