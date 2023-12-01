#!/bin/sh
alias python=python3
python manage.py migrate

# base user and first telegram bot
python manage.py shell -c "import docker_init"

# runs the server
python manage.py runserver 0.0.0.0:8000
