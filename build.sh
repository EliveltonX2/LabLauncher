#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic
python manage.py migrate
python manage.py create_superuser_from_env