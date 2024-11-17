FROM python:3.10.0-alpine

RUN apk update && apk add python3-dev gcc libc-dev musl-dev

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install uvicorn
ADD ./requirements/prod.txt /app/requirements.txt
RUN pip install -r requirements.txt

ADD ./backend /app/backend
ADD ./docker /app/docker

RUN chmod +x /app/docker/backend/django-server-entrypoint.sh
RUN chmod +x /app/docker/backend/celery-entrypoint.sh
RUN chmod +x /app/docker/backend/flower-entrypoint.sh
