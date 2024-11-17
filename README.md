# Sales Analyser
### Analyzing sales from xml file and returning a sales report

# Install dependencies (docker composer is not supported on Windows, so it can only be used on Unix systems: Linux, macOS, or WSL)
## local development:
```bash
python -m venv venv
source venv/bin/activate
```
```bash
pip install -r requirements/dev.txt  # install dev dependencies
```
```bash
pip install -r requirements/test.txt  # install test dependencies
```
```bash
cd backend
python manage.py runasgi  # running asgi server
```
## docker compose:
- [ ] [Docker и Docker Compose](https://dev.to/trueqap/how-to-install-docker-and-docker-compose-on-ubuntu-5boh) or official website: [Install Docker](https://docs.docker.com/desktop/install/linux/) и [Docker Compose](https://docs.docker.com/compose/install/)

