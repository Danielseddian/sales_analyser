# Sales Analyser
### A convenient AI-based service for analyzing sales data

## Installing dependencies
## (docker composer is not supported on Windows, so it can only be used on Unix systems: Linux, macOS, or WSL):
### on before local running:
```bash
python -m venv venv  # creating virtual environment
source venv/bin/activate  # activating virtual environment
```
```bash
pip install -r requirements/dev.txt  # installing dev dependencies
```
```bash
pip install -r requirements/test.txt  # installing test dependencies
```
```bash
cd backend  # only if console is on root project directory
python manage.py start_ngrok 8000  # creating external access point to ur local server port
```
### convenient in debug mode server running:
```bash
cd backend  # only if console is on root project directory
python manage.py runasgi  # running asgi server
```
### docker compose:
- [ ] [Docker и Docker Compose](https://dev.to/trueqap/how-to-install-docker-and-docker-compose-on-ubuntu-5boh) or official website: [Install Docker](https://docs.docker.com/desktop/install/linux/) и [Docker Compose](https://docs.docker.com/compose/install/)
```bash
sudo docker compose -f docker-compose-dev.yml up -d --build  # creating images and running containers for development
```
### on before production running it should be:
- renamed every `example.com` to ur server domain name in `<project root>`/docker/nginx/nginx.conf 
- added `ALLOWED_HOSTS` to ur server domain name in `<project root>`/.env
- set `DEBUG_MODE` to `False` or `No` in `<project root>`/.env
### server running:
```bash
sudo docker compose up -d --build  # creating images and running containers on server
```
